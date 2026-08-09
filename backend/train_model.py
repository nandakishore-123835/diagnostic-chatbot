from services.model_service import train_model


if __name__ == "__main__":
    model = train_model()
    print("Model trained successfully.")
    print(f"Vocabulary size: {len(model.get('vocabulary', []))}")
    print(f"Training documents: {len(model.get('documents', []))}")
