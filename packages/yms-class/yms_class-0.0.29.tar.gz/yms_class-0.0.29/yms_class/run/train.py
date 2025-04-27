import os
import time
from datetime import timedelta

import torch
from torch.nn import CrossEntropyLoss
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights

from yms_class.models.CNN import CNN
from yms_class.tools.dataset import create_dataloaders
from yms_class.tools.plotting import plot_all_metrics
from yms_class.tools.tool import calculate_metric, append_to_results_file, wandb_init, initialize_results_file
from yms_class.tools.train_eval_utils import train_one_epoch, eval_one_epoch


def main(args):
    # 创建输出文件夹
    save_dir = args.save_dir
    img_dir = os.path.join(save_dir, 'images')
    model_dir = os.path.join(save_dir, 'models')
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    results_file = os.path.join(save_dir, 'feature_extractor_results.txt')
    column_order = ['epoch', 'train_losses', 'val_losses', 'accuracies', 'precisions', 'recalls',
                    'f1-scores', 'lrs']
    initialize_results_file(results_file, column_order)
    custom_column_widths = {'epoch': 5, 'train_loss': 12, 'val_loss': 10, 'accuracy': 10, 'precision': 9, 'recall': 7,
                            'f1-score': 8,
                            'lr': 3}

    run = wandb_init(args.project, args.wandb_key, args.job_name)
    device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
    print("Using {} device training.".format(device.type))

    # transform = transforms.Compose([
    #     transforms.Resize((224, 224)),  # 将图像的大小调整为224x224像素
    #     transforms.ToTensor(),  # 将图像从PIL.Image格式转换为PyTorch张量格式。
    #     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # 对图像进行归一化，使其具有指定的均值和标准差。
    # ])
    train_loader, val_loader = create_dataloaders(args.data_dir, args.batch_size)
    classes = train_loader.dataset.classes
    metrics = {'train_losses': [], 'val_losses': [], 'accuracies': [], 'precisions': [], 'recalls': [], 'f1-scores': [],
               'lrs': []}

    model = CNN().to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    lr_scheduler = ReduceLROnPlateau(optimizer, 'min', factor=0.1, patience=4, min_lr=1e-9)
    criterion = CrossEntropyLoss()
    best = -1
    num_epochs = args.epochs
    start_time = time.time()
    for epoch in range(0, num_epochs):
        training_lr = lr_scheduler.get_last_lr()[0]
        train_loss, train_accuracy = train_one_epoch(model=model, train_loader=train_loader, device=device,
                                                     optimizer=optimizer, criterion=criterion, epoch=epoch)
        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.2%},'
              f'lr: {training_lr}')

        result = eval_one_epoch(model=model, val_loader=val_loader,
                                device=device, criterion=criterion, epoch=epoch)
        metric = calculate_metric(result['y_true'], result['y_pred'], classes)
        print(f'val epoch {epoch + 1}, val loss: {result["val_loss"]:.4f}, accuracy: {metric["accuracy"]:.2%}')
        metrics['train_losses'].append(train_loss)
        metrics['val_losses'].append(result['val_loss'])
        metrics['accuracies'].append(metric['accuracy'])
        metrics['precisions'].append(metric['precision'])
        metrics['recalls'].append(metric['recall'])
        metrics['f1-scores'].append(metric['f1-score'])
        metrics['lrs'].append(training_lr)

        metric.update({'epoch': epoch, 'train_loss': train_loss, 'val_loss': result['val_loss'], 'lr': training_lr})
        append_to_results_file(results_file, metric, column_order,
                               custom_column_widths=custom_column_widths)

        save_file = {
            'epoch': epoch,
            'model_state_dict': model,
            'optimizer_state_dict': optimizer,
            'lr_scheduler_state_dict': lr_scheduler,
        }
        torch.save(save_file, os.path.join(model_dir, 'last_model.pt'))
        if metric['f1-score'] > best:
            best = metric['f1-score']
            # torch.save(model, os.path.join(model_dir, 'best_model.pt'))
            model.save(os.path.join(model_dir, 'best_model.pt'))

    total_time = time.time() - start_time
    total_time_str = str(timedelta(seconds=int(total_time)))
    print('Training time {}'.format(total_time_str))
    plot_all_metrics(metrics, args.epochs, 'cnn', img_dir)
    if run is not None:
        run.finish()
    os.remove(os.path.join(model_dir, 'last_model.pt'))


def parse_args(args=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data_dir', default=r'D:\Code\2-ZSL\0-data\data\CRWU\D2')
    parser.add_argument('--save_dir', default=r'output2')
    parser.add_argument('--epochs', default=40, type=int)
    parser.add_argument('--batch_size', default=64, type=int)
    parser.add_argument('--lr', default=1e-3, type=float)
    parser.add_argument('--weight_decay', default=1e-5, type=float)
    parser.add_argument('--model_weight', default=r'')
    parser.add_argument('--num_classes', default=6, type=int)
    parser.add_argument('--project', default=None)
    parser.add_argument('--wandb_key', type=str, default='epoch')
    parser.add_argument('--job_name', type=str, default='')

    return parser.parse_args(args if args else [])


if __name__ == '__main__':
    opts = parse_args()
    print(opts)
    main(opts)
