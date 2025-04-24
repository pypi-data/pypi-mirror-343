"""
Скрипт для очистки старых лог-файлов.
"""
import os
import argparse
import logging
import datetime
from pathlib import Path
from typing import List


def setup_simple_logging():
    """Настраивает простое логирование для скрипта."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    return logging.getLogger(__name__)


def list_log_files(log_dir: str, recursive: bool = False) -> List[Path]:
    """
    Перечисляет файлы логов в директории.
    
    Args:
        log_dir: Директория с логами
        recursive: Искать файлы рекурсивно в поддиректориях
        
    Returns:
        List[Path]: Список путей к файлам логов
    """
    log_dir_path = Path(log_dir)
    if not log_dir_path.exists():
        return []
    
    if recursive:
        log_files = list(log_dir_path.glob('**/*.log*'))
    else:
        log_files = list(log_dir_path.glob('*.log*'))
        
    return log_files


def clean_old_logs(log_dir: str, days: int, dry_run: bool = False, recursive: bool = False) -> int:
    """
    Очищает старые файлы логов.
    
    Args:
        log_dir: Директория с логами
        days: Удалять файлы старше указанного количества дней
        dry_run: Только вывод информации без удаления
        recursive: Искать файлы рекурсивно в поддиректориях
        
    Returns:
        int: Количество удаленных файлов
    """
    logger = logging.getLogger(__name__)
    
    log_files = list_log_files(log_dir, recursive)
    now = datetime.datetime.now()
    cutoff_date = now - datetime.timedelta(days=days)
    
    removed_count = 0
    
    for log_file in log_files:
        # Получаем время последней модификации файла
        mtime = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
        
        # Если файл старше указанного срока, удаляем его
        if mtime < cutoff_date:
            logger.info(f"{'Would remove' if dry_run else 'Removing'} old log file: {log_file} (Last modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
            if not dry_run:
                try:
                    os.remove(log_file)
                    removed_count += 1
                except Exception as e:
                    logger.error(f"Error removing {log_file}: {e}")
    
    return removed_count


def main():
    """Основная функция скрипта."""
    parser = argparse.ArgumentParser(description='Clean old log files')
    
    parser.add_argument(
        '--log-dir', '-d',
        default='logs',
        help='Directory with log files'
    )
    
    parser.add_argument(
        '--days', '-n',
        type=int,
        default=30,
        help='Remove files older than N days'
    )
    
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Search logs recursively in subdirectories'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Only show what would be removed without actually removing'
    )
    
    args = parser.parse_args()
    
    logger = setup_simple_logging()
    
    logger.info(f"Cleaning log files in {args.log_dir} older than {args.days} days")
    
    removed_count = clean_old_logs(args.log_dir, args.days, args.dry_run, args.recursive)
    
    if args.dry_run:
        logger.info(f"Would remove {removed_count} old log files")
    else:
        logger.info(f"Removed {removed_count} old log files")


if __name__ == "__main__":
    main() 