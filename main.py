import cv2
import numpy as np
import os
from pathlib import Path
import json
from datetime import datetime

class VideoQuantizer:
    """Основной класс для обработки видео с использованием GPU"""
    
    def __init__(self, n_quants=4, output_dir="output"):
        """
        Args:
            n_quants: Количество квантов (4-10)
            output_dir: Директория для сохранения результатов
        """
        self.n_quants = n_quants
        self.output_dir = output_dir
        self.results = {
            'input_file': None,
            'frames_count': 0,
            'frame_shape': None,
            'n_quants': n_quants,
            'processing_time': 0,
            'method': None
        }
        os.makedirs(output_dir, exist_ok=True)
        
    def load_video(self, video_path, max_frames=None):
        """Загрузить видеофайл в виде массива кадров"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if max_frames:
            total_frames = min(total_frames, max_frames)
        
        frames = []
        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        
        self.results['input_file'] = video_path
        self.results['frames_count'] = len(frames)
        self.results['frame_shape'] = frames[0].shape if frames else None
        
        return np.array(frames), fps, (width, height)
    
    def quantize_frame_cpu(self, frame):
        """Квантование кадра на CPU"""
        frame = frame.astype(np.float32)
        
        # Вычисляем шаг квантования
        step = 256 // self.n_quants
        
        # Для каждого пикселя находим значение из центра кванта
        quantized = np.zeros_like(frame)
        
        for channel in range(frame.shape[2]):
            channel_data = frame[:, :, channel]
            quant_indices = (channel_data / step).astype(np.int32)
            quant_indices = np.clip(quant_indices, 0, self.n_quants - 1)
            quantized[:, :, channel] = (quant_indices + 0.5) * step
        
        return np.clip(quantized, 0, 255).astype(np.uint8)
    
    def process_video_cpu(self, frames):
        """Обработать все кадры на CPU"""
        processed_frames = []
        for frame in frames:
            quantized = self.quantize_frame_cpu(frame)
            processed_frames.append(quantized)
        return np.array(processed_frames)
    
    def save_video(self, frames, output_path, fps, frame_size):
        """Сохранить обработанные кадры в видеофайл"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
        
        for frame in frames:
            out.write(frame)
        
        out.release()
    
    def save_frames_as_images(self, frames, output_dir):
        """Сохранить кадры как изображения"""
        os.makedirs(output_dir, exist_ok=True)
        for i, frame in enumerate(frames):
            cv2.imwrite(f"{output_dir}/frame_{i:04d}.png", frame)
    
    def create_comparison_image(self, original, processed, output_path):
        """Создать изображение сравнения оригинального и обработанного кадра"""
        h, w = original.shape[:2]
        comparison = np.zeros((h, w * 2 + 10, 3), dtype=np.uint8)
        comparison[:, :w] = original
        comparison[:, w+10:] = processed;
        
        # Добавить текст
        cv2.putText(comparison, 'Original', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(comparison, f'Quantized (n={self.n_quants})', (w + 20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imwrite(output_path, comparison)
    
    def get_histogram_stats(self, frames):
        """Получить статистику гистограмм кадров"""
        stats = {
            'original': [],
            'processed': []
        }
        return stats


def main():
    print("=== GPU Video Processing with Color Quantization ===")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Параметры
    n_quants = 6  # Количество квантов
    test_videos = []  # Будут подготовлены позже
    
    print(f"\nQuantization levels: {n_quants}")
    print(f"Output directory: output")

if __name__ == "__main__":
    main()