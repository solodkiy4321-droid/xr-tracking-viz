import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from parser import load_tracking_data

def plot_trajectories(df, output_path='results/trajectories_3d.png'):
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    times = df['time'].values
    colors = times - times.min()

    # Голова
    if 'head_x' in df.columns:
        ax.scatter(
            df['head_x'], df['head_y'], df['head_z'],
            c=colors, cmap='viridis', s=8, alpha=0.7, label='Head'
        )
        # Стартовая точка
        ax.scatter(
            df['head_x'].iloc[0], df['head_y'].iloc[0], df['head_z'].iloc[0],
            c='red', s=80, marker='o', edgecolors='black', label='Start'
        )

    # Левая рука
    if 'left_wrist_x' in df.columns:
        mask = df['left_wrist_x'].notna()
        ax.scatter(
            df.loc[mask, 'left_wrist_x'],
            df.loc[mask, 'left_wrist_y'],
            df.loc[mask, 'left_wrist_z'],
            c=colors[mask], cmap='plasma', s=6, alpha=0.5,
            label='Left wrist'
        )

    # Правая рука
    if 'right_wrist_x' in df.columns:
        mask = df['right_wrist_x'].notna()
        ax.scatter(
            df.loc[mask, 'right_wrist_x'],
            df.loc[mask, 'right_wrist_y'],
            df.loc[mask, 'right_wrist_z'],
            c=colors[mask], cmap='plasma', s=6, alpha=0.5,
            label='Right wrist'
        )

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('VR Tracking: 3D Trajectories (color = time)')
    ax.legend(loc='upper left')

    # colorbar для времени
    sm = plt.cm.ScalarMappable(cmap='viridis')
    sm.set_array(colors)
    cbar = plt.colorbar(sm, ax=ax, shrink=0.6)
    cbar.set_label('Time (s from start)')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Сохранено: {output_path}")


def plot_timeseries(df, output_path='results/position_timeseries.png'):
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    for i, axis in enumerate(['x', 'y', 'z']):
        if f'head_{axis}' in df.columns:
            axes[i].plot(df['time'], df[f'head_{axis}'], label='Head', alpha=0.8)
        if f'left_wrist_{axis}' in df.columns:
            axes[i].plot(df['time'], df[f'left_wrist_{axis}'], label='Left wrist', alpha=0.8)
        if f'right_wrist_{axis}' in df.columns:
            axes[i].plot(df['time'], df[f'right_wrist_{axis}'], label='Right wrist', alpha=0.8)
        axes[i].set_ylabel(f'{axis.upper()} (m)')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)

    axes[-1].set_xlabel('Time (s)')
    plt.suptitle('Position over Time')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Сохранено: {output_path}")


if __name__ == '__main__':
    df, camera_info = load_tracking_data('data/trackingData_20260505_165740.txt')
    print(f"Кадров: {len(df)}")
    plot_trajectories(df)
    plot_timeseries(df)