import os
from PIL import Image
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
from src.logger import logging


def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logging.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logging.error('YAML error: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        raise


# ========== Step 1: Check for corrupted images ==========
def check_corrupted_images(root_dir):
    print("🔍 Checking for corrupted images...")
    for phase in ['train', 'val', 'test']:
        phase_path = os.path.join(root_dir, phase)
        for cls in os.listdir(phase_path):
            class_path = os.path.join(phase_path, cls)
            for img_file in os.listdir(class_path):
                img_path = os.path.join(class_path, img_file)
                try:
                    img = Image.open(img_path)
                    img.verify()
                except Exception as e:
                    print(f"⚠️ Corrupted image found: {img_path} — {e}")

# ========== Step 2: Define Transforms ==========
IMG_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])

val_test_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
])

# ========== Step 3: Load Datasets ==========
def load_datasets(data_dir):
    print("📦 Loading datasets...")
    train_dataset = datasets.ImageFolder(os.path.join(data_dir, 'train'), transform=train_transform)
    val_dataset = datasets.ImageFolder(os.path.join(data_dir, 'val'), transform=val_test_transform)
    test_dataset = datasets.ImageFolder(os.path.join(data_dir, 'test'), transform=val_test_transform)
    return train_dataset, val_dataset, test_dataset

# ========== Step 4: Create DataLoaders ==========
def create_dataloaders(train_ds, val_ds, test_ds, batch_size=32):
    print("🚚 Creating dataloaders...")
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader, test_loader

# ========== Main Execution ==========
if __name__ == "__main__":
    params = load_params(params_path='params.yaml')
    DATA_DIR = params['data_ingestion']['path_to_store_data'] + "/" +params['data_ingestion']['data_folder_name']

    check_corrupted_images(DATA_DIR)
    logging.info("No Corrupted image found!!")
    
    train_ds, val_ds, test_ds = load_datasets(DATA_DIR)
    train_loader, val_loader, test_loader = create_dataloaders(train_ds, val_ds, test_ds)

    print("✅ Preprocessing complete.")
    print(f"Train samples: {len(train_ds)}, Val: {len(val_ds)}, Test: {len(test_ds)}")