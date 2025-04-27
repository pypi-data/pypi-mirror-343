"""
Các lệnh quản lý file trên thiết bị Android.
"""

import os
import logging
from typing import Optional, List, Dict, Any

from ..exceptions import ADBCommandError, FileOperationError

logger = logging.getLogger('my_adb_lib')

class FileCommands:
    """
    Lớp chứa các lệnh quản lý file trên thiết bị Android.
    """
    
    def __init__(self, adb_runner):
        """
        Khởi tạo đối tượng FileCommands.
        
        Args:
            adb_runner: Đối tượng thực thi lệnh ADB
        """
        self.adb = adb_runner
    
    def push(self, local_path: str, remote_path: str) -> str:
        """
        Đẩy file từ máy tính lên thiết bị.
        
        Args:
            local_path: Đường dẫn file trên máy tính
            remote_path: Đường dẫn đích trên thiết bị
            
        Returns:
            Kết quả lệnh
            
        Raises:
            FileOperationError: Nếu thao tác thất bại
        """
        if not os.path.exists(local_path):
            raise FileOperationError("push", local_path, remote_path, "File nguồn không tồn tại")
        
        try:
            logger.debug(f"Pushing file from {local_path} to {remote_path}")
            return self.adb.run(f"push {local_path} {remote_path}")
        except ADBCommandError as e:
            raise FileOperationError("push", local_path, remote_path, e.error_message)
    
    def pull(self, remote_path: str, local_path: str) -> str:
        """
        Lấy file từ thiết bị về máy tính.
        
        Args:
            remote_path: Đường dẫn file trên thiết bị
            local_path: Đường dẫn đích trên máy tính
            
        Returns:
            Kết quả lệnh
            
        Raises:
            FileOperationError: Nếu thao tác thất bại
        """
        try:
            logger.debug(f"Pulling file from {remote_path} to {local_path}")
            return self.adb.run(f"pull {remote_path} {local_path}")
        except ADBCommandError as e:
            raise FileOperationError("pull", remote_path, local_path, e.error_message)
    
    def run_as(self, package: str, file_path: str) -> str:
        """
        Đọc file trong sandbox của ứng dụng.
        
        Args:
            package: Tên package của ứng dụng
            file_path: Đường dẫn file trong sandbox
            
        Returns:
            Nội dung file
            
        Raises:
            FileOperationError: Nếu thao tác thất bại
        """
        try:
            logger.debug(f"Reading file {file_path} as package {package}")
            return self.adb.run(f"shell run-as {package} cat {file_path}")
        except ADBCommandError as e:
            raise FileOperationError("run-as", file_path, error_message=e.error_message)
    
    def ls(self, remote_path: str) -> List[str]:
        """
        Liệt kê các file và thư mục trong đường dẫn.
        
        Args:
            remote_path: Đường dẫn trên thiết bị
            
        Returns:
            Danh sách tên file và thư mục
        """
        try:
            logger.debug(f"Listing files in {remote_path}")
            output = self.adb.run(f"shell ls -la {remote_path}")
            files = []
            
            for line in output.splitlines():
                if not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) >= 8:
                    # Format: permissions links owner group size date time name
                    file_name = ' '.join(parts[8:])
                    files.append(file_name)
            
            return files
        except ADBCommandError as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    def mkdir(self, remote_path: str) -> str:
        """
        Tạo thư mục trên thiết bị.
        
        Args:
            remote_path: Đường dẫn thư mục cần tạo
            
        Returns:
            Kết quả lệnh
        """
        logger.debug(f"Creating directory {remote_path}")
        return self.adb.run(f"shell mkdir -p {remote_path}")
    
    def rm(self, remote_path: str, recursive: bool = False) -> str:
        """
        Xóa file hoặc thư mục trên thiết bị.
        
        Args:
            remote_path: Đường dẫn cần xóa
            recursive: Xóa đệ quy (cho thư mục)
            
        Returns:
            Kết quả lệnh
        """
        cmd = f"shell rm {'-r' if recursive else ''} {remote_path}"
        logger.debug(f"Removing {remote_path}")
        return self.adb.run(cmd)
    
    def cat(self, remote_path: str) -> str:
        """
        Đọc nội dung file trên thiết bị.
        
        Args:
            remote_path: Đường dẫn file cần đọc
            
        Returns:
            Nội dung file
        """
        logger.debug(f"Reading file {remote_path}")
        return self.adb.run(f"shell cat {remote_path}")
    
    def write_file(self, remote_path: str, content: str) -> str:
        """
        Ghi nội dung vào file trên thiết bị.
        
        Args:
            remote_path: Đường dẫn file cần ghi
            content: Nội dung cần ghi
            
        Returns:
            Kết quả lệnh
        """
        # Escape content for shell
        content = content.replace('"', '\\"').replace('$', '\\$')
        logger.debug(f"Writing to file {remote_path}")
        return self.adb.run(f'shell "echo -n \\"{content}\\" > {remote_path}"')
    
    def append_file(self, remote_path: str, content: str) -> str:
        """
        Thêm nội dung vào cuối file trên thiết bị.
        
        Args:
            remote_path: Đường dẫn file cần thêm
            content: Nội dung cần thêm
            
        Returns:
            Kết quả lệnh
        """
        # Escape content for shell
        content = content.replace('"', '\\"').replace('$', '\\$')
        logger.debug(f"Appending to file {remote_path}")
        return self.adb.run(f'shell "echo -n \\"{content}\\" >> {remote_path}"')
    
    def chmod(self, remote_path: str, mode: str) -> str:
        """
        Thay đổi quyền truy cập file trên thiết bị.
        
        Args:
            remote_path: Đường dẫn file cần thay đổi quyền
            mode: Chế độ quyền (ví dụ: "755")
            
        Returns:
            Kết quả lệnh
        """
        logger.debug(f"Changing permissions of {remote_path} to {mode}")
        return self.adb.run(f"shell chmod {mode} {remote_path}")
    
    def cp(self, source_path: str, dest_path: str) -> str:
        """
        Sao chép file trên thiết bị.
        
        Args:
            source_path: Đường dẫn nguồn
            dest_path: Đường dẫn đích
            
        Returns:
            Kết quả lệnh
        """
        logger.debug(f"Copying {source_path} to {dest_path}")
        return self.adb.run(f"shell cp {source_path} {dest_path}")
    
    def mv(self, source_path: str, dest_path: str) -> str:
        """
        Di chuyển file trên thiết bị.
        
        Args:
            source_path: Đường dẫn nguồn
            dest_path: Đường dẫn đích
            
        Returns:
            Kết quả lệnh
        """
        logger.debug(f"Moving {source_path} to {dest_path}")
        return self.adb.run(f"shell mv {source_path} {dest_path}")
    
    def file_exists(self, remote_path: str) -> bool:
        """
        Kiểm tra xem file có tồn tại trên thiết bị không.
        
        Args:
            remote_path: Đường dẫn file cần kiểm tra
            
        Returns:
            True nếu file tồn tại, False nếu không
        """
        try:
            logger.debug(f"Checking if file exists: {remote_path}")
            output = self.adb.run(f"shell [ -e {remote_path} ] && echo 'exists' || echo 'not exists'")
            return "exists" in output
        except ADBCommandError:
            return False
    
    def is_directory(self, remote_path: str) -> bool:
        """
        Kiểm tra xem đường dẫn có phải là thư mục không.
        
        Args:
            remote_path: Đường dẫn cần kiểm tra
            
        Returns:
            True nếu là thư mục, False nếu không
        """
        try:
            logger.debug(f"Checking if path is directory: {remote_path}")
            output = self.adb.run(f"shell [ -d {remote_path} ] && echo 'dir' || echo 'not dir'")
            return "dir" in output
        except ADBCommandError:
            return False
    
    def get_file_size(self, remote_path: str) -> int:
        """
        Lấy kích thước file trên thiết bị.
        
        Args:
            remote_path: Đường dẫn file cần kiểm tra
            
        Returns:
            Kích thước file (bytes)
        """
        try:
            logger.debug(f"Getting file size: {remote_path}")
            output = self.adb.run(f"shell stat -c %s {remote_path}")
            return int(output.strip())
        except (ADBCommandError, ValueError):
            return -1
    
    def get_file_permissions(self, remote_path: str) -> str:
        """
        Lấy quyền truy cập file trên thiết bị.
        
        Args:
            remote_path: Đường dẫn file cần kiểm tra
            
        Returns:
            Chuỗi quyền truy cập (ví dụ: "rwxr-xr-x")
        """
        try:
            logger.debug(f"Getting file permissions: {remote_path}")
            output = self.adb.run(f"shell stat -c %A {remote_path}")
            return output.strip()
        except ADBCommandError:
            return ""
    
    def get_file_info(self, remote_path: str) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết về file trên thiết bị.
        
        Args:
            remote_path: Đường dẫn file cần kiểm tra
            
        Returns:
            Dictionary chứa thông tin file
        """
        try:
            logger.debug(f"Getting file info: {remote_path}")
            output = self.adb.run(f"shell ls -la {remote_path}")
            
            if not output or "No such file or directory" in output:
                return {}
            
            lines = output.splitlines()
            if len(lines) < 1:
                return {}
            
            # For directories, we might get multiple lines
            line = lines[0]
            if remote_path.endswith("/") and len(lines) > 1:
                # Find the line that corresponds to the directory itself (usually has ".")
                for l in lines:
                    if " . " in l or " ./" in l or l.endswith(" ."):
                        line = l
                        break
            
            parts = line.split()
            if len(parts) < 8:
                return {}
            
            info = {
                "path": remote_path,
                "permissions": parts[0],
                "owner": parts[2],
                "group": parts[3],
                "size": int(parts[4]) if parts[4].isdigit() else parts[4],
                "modified": f"{parts[5]} {parts[6]} {parts[7]}",
                "is_directory": parts[0].startswith("d")
            }
            
            return info
        
        except ADBCommandError:
            return {}
    
    def sync(self, local_dir: str, remote_dir: str, direction: str = "push") -> str:
        """
        Đồng bộ hóa thư mục giữa máy tính và thiết bị.
        
        Args:
            local_dir: Đường dẫn thư mục trên máy tính
            remote_dir: Đường dẫn thư mục trên thiết bị
            direction: Hướng đồng bộ ("push" hoặc "pull")
            
        Returns:
            Kết quả lệnh
        """
        if direction not in ["push", "pull"]:
            raise ValueError("Direction must be 'push' or 'pull'")
        
        if direction == "push":
            logger.debug(f"Syncing from {local_dir} to {remote_dir}")
            return self.adb.run(f"sync {local_dir} {remote_dir}")
        else:
            logger.debug(f"Syncing from {remote_dir} to {local_dir}")
            return self.adb.run(f"sync {remote_dir} {local_dir}")
