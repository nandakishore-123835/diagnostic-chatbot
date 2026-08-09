import json
import math
import os
import re


class T5Model:

    def __init__(self, artifact_path=None):
        self.artifact_path = artifact_path or os.path.join(
            os.path.dirname(__file__),
            "artifacts",
            "diagnostic_model.json"
        )
        self.model = None
        self.tokenizer = None

    def load_model(self):
        if self.model is not None:
            return self.model

        if os.path.exists(self.artifact_path):
            with open(self.artifact_path, "r", encoding="utf-8") as file:
                self.model = json.load(file)
            return self.model

        return self.train_model()

    def train_model(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "dtc_codes.json")

        with open(data_path, "r", encoding="utf-8") as file:
            dtc_data = json.load(file)

        documents = []
        vocabulary = set()

        for entry in dtc_data:
            text = self._build_training_text(entry)
            tokens = self._tokenize(text)
            vocabulary.update(tokens)
            documents.append({
                "code": entry["code"],
                "title": entry["title"],
                "description": entry["description"],
                "symptoms": entry.get("symptoms", []),
                "possible_causes": entry.get("possible_causes", []),
                "severity": entry.get("severity", "Unknown"),
                "tokens": tokens,
            })

        vocabulary = sorted(vocabulary)
        document_frequencies = {token: 0 for token in vocabulary}
        for document in documents:
            for token in set(document["tokens"]):
                document_frequencies[token] += 1

        total_documents = max(len(documents), 1)
        for document in documents:
            document["vector"] = self._vectorize(document["tokens"], vocabulary, document_frequencies, total_documents)

        artifact = {
            "version": 1,
            "vocabulary": vocabulary,
            "documents": documents,
        }

        os.makedirs(os.path.dirname(self.artifact_path), exist_ok=True)
        with open(self.artifact_path, "w", encoding="utf-8") as file:
            json.dump(artifact, file, ensure_ascii=False, indent=2)

        self.model = artifact
        return artifact

    def generate_response(self, prompt):
        model = self.load_model()
        documents = model.get("documents", [])

        parsed = self._parse_prompt(prompt)
        query_text = parsed.get("query") or prompt
        query_code = self._extract_code(query_text)
        if not query_code:
            query_code = self._extract_code(prompt)

        if query_code:
            for document in documents:
                if document["code"].upper() == query_code.upper():
                    return self._format_response(document, query_text, exact_match=True)

        vocabulary = model.get("vocabulary", [])
        query_tokens = self._tokenize(query_text)
        query_vector = self._vectorize(query_tokens, vocabulary, None, None)

        best_document = None
        best_score = 0.0
        for document in documents:
            score = self._cosine_similarity(query_vector, document.get("vector", []))
            if score > best_score:
                best_score = score
                best_document = document

        if best_document and best_score >= 0.15:
            return self._format_response(best_document, query_text, similarity=best_score)

        return (
            "I could not confidently match the issue to a known diagnostic code. "
            "Please provide the check engine code, warning light details, and symptoms, "
            "and I will narrow it down."
        )

    def _build_training_text(self, entry):
        parts = [
            entry.get("code", ""),
            entry.get("title", ""),
            entry.get("description", ""),
            " ".join(entry.get("symptoms", [])),
            " ".join(entry.get("possible_causes", [])),
            entry.get("severity", ""),
        ]
        return " ".join(part for part in parts if part)

    def _parse_prompt(self, prompt):
        query_match = re.search(r"User question:\s*(.*?)(?:\n\n|Diagnostic code:|$)", prompt, re.DOTALL | re.IGNORECASE)
        query = query_match.group(1).strip() if query_match else prompt.strip()

        code_match = re.search(r"Diagnostic code:\s*(\w+)", prompt, re.IGNORECASE)
        title_match = re.search(r"Problem:\s*(.*?)(?:\n\nDescription:|$)", prompt, re.DOTALL | re.IGNORECASE)
        description_match = re.search(r"Description:\s*(.*?)(?:\n\nPossible causes:|$)", prompt, re.DOTALL | re.IGNORECASE)
        causes_match = re.search(r"Possible causes:\s*(.*?)(?:\n\nSymptoms:|$)", prompt, re.DOTALL | re.IGNORECASE)
        symptoms_match = re.search(r"Symptoms:\s*(.*?)(?:\n\nProvide a clear|$)", prompt, re.DOTALL | re.IGNORECASE)

        return {
            "query": query,
            "code": code_match.group(1).strip() if code_match else None,
            "title": title_match.group(1).strip() if title_match else None,
            "description": description_match.group(1).strip() if description_match else None,
            "possible_causes": [part.strip() for part in causes_match.group(1).split(",") if part.strip()] if causes_match else [],
            "symptoms": [part.strip() for part in symptoms_match.group(1).split(",") if part.strip()] if symptoms_match else [],
        }

    def _extract_code(self, text):
        match = re.search(r"\b[PCBU][0-9]{4}\b", text.upper())
        return match.group(0) if match else None

    def _tokenize(self, text):
        return re.findall(r"[a-z0-9]+", text.lower())

    def _vectorize(self, tokens, vocabulary, document_frequencies, total_documents):
        if not vocabulary:
            return []

        counts = {}
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1

        vector = []
        for token in vocabulary:
            term_frequency = counts.get(token, 0)
            if not term_frequency:
                vector.append(0.0)
                continue

            if document_frequencies is None or total_documents is None:
                vector.append(float(term_frequency))
                continue

            inverse_document_frequency = math.log((1 + total_documents) / (1 + document_frequencies.get(token, 0))) + 1
            vector.append(float(term_frequency) * inverse_document_frequency)

        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            vector = [value / norm for value in vector]

        return vector

    def _cosine_similarity(self, left_vector, right_vector):
        if not left_vector or not right_vector:
            return 0.0

        return sum(left * right for left, right in zip(left_vector, right_vector))

    def _format_response(self, document, query_text, exact_match=False, similarity=None):
        reason = "Exact diagnostic code match" if exact_match else "Closest trained diagnosis"
        if similarity is not None:
            reason = f"Closest trained diagnosis ({similarity:.2f} similarity)"

        symptoms = ", ".join(document.get("symptoms", [])) or "Not listed"
        causes = ", ".join(document.get("possible_causes", [])) or "Not listed"

        return (
            f"{reason}: {document['code']} - {document['title']}. "
            f"{document['description']} Possible causes include {causes}. "
            f"Common symptoms include {symptoms}. Severity: {document.get('severity', 'Unknown')}."
        )