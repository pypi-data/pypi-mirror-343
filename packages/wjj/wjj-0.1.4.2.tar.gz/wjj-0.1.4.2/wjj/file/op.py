import stat
import os
import shutil


def copy_file_as(src_path: str, dst_path: str, overwrite: bool = False) -> str:
    """
    将源路径复制为指定目标路径，严格保持类型一致
    (文件 -> 文件 / 目录 -> 目录)

    :param src_path: 源路径（文件或目录）
    :param dst_path: 目标完整路径
    :param overwrite: 是否覆盖已有内容
    :return: 最终存储路径
    """
    # 校验源路径
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"源路径不存在: {src_path}")

    # 类型一致性校验
    src_is_file = os.path.isfile(src_path)
    if os.path.exists(dst_path):
        dst_is_file = os.path.isfile(dst_path)
        if src_is_file != dst_is_file:
            type_error = f"类型冲突: 无法将 {'文件' if src_is_file else '目录'} 复制为 {'文件' if dst_is_file else '目录'}"
            raise TypeError(type_error)

    # 处理目标路径存在的情况
    if os.path.exists(dst_path):
        if not overwrite:
            raise FileExistsError(f"目标路径已存在: {dst_path}")

        # 删除已有目标
        if os.path.isfile(dst_path):
            os.remove(dst_path)
        else:
            shutil.rmtree(dst_path)

    # 执行复制操作
    try:
        if src_is_file:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)  # 保留元数据
        else:
            # 自动创建父目录
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copytree(
                src_path,
                dst_path,
                copy_function=shutil.copy2,
                dirs_exist_ok=False  # 已提前处理覆盖逻辑
            )
    except shutil.Error as e:
        raise RuntimeError(f"复制失败: {str(e)}") from e

    return dst_path

def copy_item(src_path: str, dst_dir: str, overwrite: bool = False) -> str:
    """
    复制文件/目录到目标目录
    :param src_path: 源路径（文件/目录）
    :param dst_dir: 目标目录
    :param overwrite: 是否覆盖已存在内容
    :return: 最终存储路径
    """
    # 校验源路径
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"源路径不存在: {src_path}")

    # 创建目标目录
    os.makedirs(dst_dir, exist_ok=True)

    # 构造目标完整路径
    base_name = os.path.basename(src_path)
    dst_path = os.path.join(dst_dir, base_name)

    # 处理已存在目标
    if os.path.exists(dst_path):
        if not overwrite:
            raise FileExistsError(f"目标路径已存在: {dst_path}")
        delete_item(dst_path)  # 先删除已有内容

    # 执行复制
    try:
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)  # 保留元数据
        else:
            shutil.copytree(src_path, dst_path,
                            dirs_exist_ok=overwrite,  # Python 3.8+ 特性
                            copy_function=shutil.copy2)
    except shutil.Error as e:
        raise RuntimeError(f"复制过程中发生错误: {str(e)}") from e

    return dst_path


def delete_item(target_path: str) -> None:
    """
    删除文件/目录
    :param target_path: 目标路径
    """
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"目标路径不存在: {target_path}")

    def on_error(func, path, exc_info):
        """处理只读文件删除"""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    try:
        if os.path.isfile(target_path):
            os.remove(target_path)
        else:
            shutil.rmtree(target_path, onerror=on_error)
    except PermissionError as e:
        raise PermissionError(f"删除权限不足: {target_path}") from e


def move_item(src_path: str, dst_dir: str, overwrite: bool = False) -> str:
    """
    移动文件/目录到目标目录
    :param src_path: 源路径（文件/目录）
    :param dst_dir: 目标目录
    :param overwrite: 是否覆盖已存在内容
    :return: 最终存储路径
    """
    # 校验源路径
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"源路径不存在: {src_path}")

    # 创建目标目录
    os.makedirs(dst_dir, exist_ok=True)

    # 构造目标完整路径
    base_name = os.path.basename(src_path)
    dst_path = os.path.join(dst_dir, base_name)

    # 处理已存在目标
    if os.path.exists(dst_path):
        if not overwrite:
            raise FileExistsError(f"目标路径已存在: {dst_path}")
        delete_item(dst_path)  # 先删除已有内容

    try:
        # 执行移动操作
        shutil.move(src_path, dst_path)
    except shutil.Error as e:
        # 回退策略：尝试复制后删除
        try:
            copy_item(src_path, dst_dir, overwrite)
            delete_item(src_path)
        except Exception as fallback_e:
            raise RuntimeError(
                f"移动失败且回退失败: {str(e)} -> {str(fallback_e)}"
            ) from fallback_e

    return dst_path