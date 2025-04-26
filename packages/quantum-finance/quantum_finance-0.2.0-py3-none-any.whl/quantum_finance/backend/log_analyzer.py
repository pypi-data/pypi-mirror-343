import re


def analyze_log_file(log_filename='training_loop.log'):
    losses = []
    update_magnitudes = []
    learning_rates = []

    with open(log_filename, 'r') as f:
        for line in f:
            # Extract Loss values
            loss_match = re.search(r'Loss:\s*([0-9.]+)', line)
            if loss_match:
                losses.append(float(loss_match.group(1)))
            
            # Extract Update Magnitude values
            update_match = re.search(r'Update magnitude \(L2 norm\):\s*([0-9.]+)', line)
            if update_match:
                update_magnitudes.append(float(update_match.group(1)))
            
            # Extract Learning Rate information from various messages
            if "increasing learning rate" in line or "decreasing learning rate" in line or "Learning rate remains" in line:
                lr_match = re.search(r'Learning rate (?:remains at|too low; increasing learning rate to|too high; decreasing learning rate to)\s*([0-9.]+)', line)
                if lr_match:
                    learning_rates.append(float(lr_match.group(1)))

    num_epochs = len(losses)
    avg_loss = sum(losses) / num_epochs if num_epochs > 0 else 0
    avg_update = sum(update_magnitudes) / len(update_magnitudes) if update_magnitudes else 0
    final_lr = learning_rates[-1] if learning_rates else None

    print("Log Analysis Summary:")
    print("Total epochs logged:", num_epochs)
    print("Average Loss: {:.4f}".format(avg_loss))
    print("Average Update Magnitude (L2 norm): {:.6f}".format(avg_update))
    if final_lr is not None:
        print("Final Learning Rate: {:.6f}".format(final_lr))
    else:
        print("No Learning Rate info found.")


if __name__ == '__main__':
    analyze_log_file() 