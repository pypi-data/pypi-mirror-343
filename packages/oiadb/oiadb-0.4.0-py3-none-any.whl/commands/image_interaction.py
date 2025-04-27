"""
Các lệnh tương tác với thiết bị Android dựa trên nhận diện hình ảnh.
"""

from typing import Optional, Tuple, List, Dict, Any, Union
import logging
import os

from ..exceptions import ADBCommandError
from ..utils.advanced import CommandResult
from ..utils.image_recognition import ImageRecognition

logger = logging.getLogger('oiadb')

class ImageInteractionCommands:
    """
    Lớp chứa các lệnh tương tác với thiết bị Android dựa trên nhận diện hình ảnh.
    Hỗ trợ tìm kiếm và tương tác với hình ảnh trên nhiều loại màn hình với các điều kiện khác nhau
    (phân giải cao/thấp, hình ảnh nét/mờ/vỡ).
    """
    
    def __init__(self, adb_runner):
        """
        Khởi tạo đối tượng ImageInteractionCommands.
        
        Args:
            adb_runner: Đối tượng thực thi lệnh ADB
        """
        self.adb = adb_runner
        self.image_recognition = ImageRecognition(adb_runner)
    
    def find_image(self, template_path: str, threshold: float = 0.8, 
                  region: Optional[Tuple[int, int, int, int]] = None,
                  scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                  rotation_range: Tuple[float, float] = (0, 0), rotation_steps: int = 1,
                  use_gray: bool = True, use_canny: bool = False) -> Optional[Tuple[int, int, float]]:
        """
        Tìm hình ảnh mẫu trên màn hình thiết bị.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            threshold: Ngưỡng tương đồng (0.0 - 1.0), cao hơn = chính xác hơn
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            rotation_range: Phạm vi góc xoay để tìm kiếm (min_angle, max_angle) tính bằng độ
            rotation_steps: Số bước góc xoay trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            
        Returns:
            Tuple (x, y, confidence) hoặc None nếu không tìm thấy
        """
        logger.debug(f"Tìm hình ảnh: {template_path}")
        return self.image_recognition.find_image(
            template_path=template_path,
            threshold=threshold,
            multiple=False,
            region=region,
            scale_range=scale_range,
            rotation_range=rotation_range,
            rotation_steps=rotation_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
    
    def find_all_images(self, template_path: str, threshold: float = 0.8, 
                       region: Optional[Tuple[int, int, int, int]] = None,
                       scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                       use_gray: bool = True, use_canny: bool = False) -> List[Tuple[int, int, float]]:
        """
        Tìm tất cả các vị trí của hình ảnh mẫu trên màn hình.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            
        Returns:
            Danh sách các tuple (x, y, confidence) hoặc danh sách rỗng nếu không tìm thấy
        """
        logger.debug(f"Tìm tất cả hình ảnh: {template_path}")
        return self.image_recognition.find_all_images(
            template_path=template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
    
    def tap_image(self, template_path: str, threshold: float = 0.8, 
                 region: Optional[Tuple[int, int, int, int]] = None,
                 scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                 use_gray: bool = True, use_canny: bool = False,
                 tap_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Tìm hình ảnh trên màn hình và nhấp vào vị trí tìm thấy.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            tap_offset: Độ lệch (dx, dy) khi nhấp chuột so với tâm hình ảnh
            
        Returns:
            True nếu tìm thấy và nhấp thành công, False nếu không
        """
        logger.debug(f"Nhấp vào hình ảnh: {template_path}")
        return self.image_recognition.find_and_click(
            template_path=template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny,
            click_offset=tap_offset
        )
    
    def wait_and_tap_image(self, template_path: str, timeout: int = 10, interval: float = 0.5,
                          threshold: float = 0.8, region: Optional[Tuple[int, int, int, int]] = None,
                          scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                          use_gray: bool = True, use_canny: bool = False,
                          tap_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Đợi cho đến khi hình ảnh xuất hiện trên màn hình và nhấp vào vị trí đó.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            timeout: Thời gian tối đa đợi (giây)
            interval: Khoảng thời gian giữa các lần tìm kiếm (giây)
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            tap_offset: Độ lệch (dx, dy) khi nhấp chuột so với tâm hình ảnh
            
        Returns:
            True nếu tìm thấy và nhấp thành công, False nếu hết thời gian chờ
        """
        logger.debug(f"Đợi và nhấp vào hình ảnh: {template_path}")
        return self.image_recognition.wait_and_click(
            template_path=template_path,
            timeout=timeout,
            interval=interval,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny,
            click_offset=tap_offset
        )
    
    def tap_all_images(self, template_path: str, threshold: float = 0.8,
                      region: Optional[Tuple[int, int, int, int]] = None,
                      scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                      use_gray: bool = True, use_canny: bool = False,
                      tap_offset: Tuple[int, int] = (0, 0),
                      tap_delay: float = 0.5) -> int:
        """
        Tìm tất cả các vị trí của hình ảnh mẫu trên màn hình và nhấp vào từng vị trí.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            tap_offset: Độ lệch (dx, dy) khi nhấp chuột so với tâm hình ảnh
            tap_delay: Thời gian chờ giữa các lần nhấp (giây)
            
        Returns:
            Số lượng vị trí đã nhấp
        """
        logger.debug(f"Nhấp vào tất cả hình ảnh: {template_path}")
        return self.image_recognition.find_and_click_all(
            template_path=template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny,
            click_offset=tap_offset,
            click_delay=tap_delay
        )
    
    def wait_for_image(self, template_path: str, timeout: int = 10, interval: float = 0.5, 
                      threshold: float = 0.8, region: Optional[Tuple[int, int, int, int]] = None,
                      scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                      use_gray: bool = True, use_canny: bool = False) -> Optional[Tuple[int, int, float]]:
        """
        Đợi cho đến khi hình ảnh xuất hiện trên màn hình.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            timeout: Thời gian tối đa đợi (giây)
            interval: Khoảng thời gian giữa các lần tìm kiếm (giây)
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            
        Returns:
            Tuple (x, y, confidence) hoặc None nếu hết thời gian chờ
        """
        logger.debug(f"Đợi hình ảnh xuất hiện: {template_path}")
        return self.image_recognition.wait_for_image(
            template_path=template_path,
            timeout=timeout,
            interval=interval,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
    
    def wait_until_image_disappears(self, template_path: str, timeout: int = 10, interval: float = 0.5,
                                   threshold: float = 0.8, region: Optional[Tuple[int, int, int, int]] = None,
                                   scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                                   use_gray: bool = True, use_canny: bool = False) -> bool:
        """
        Đợi cho đến khi hình ảnh biến mất khỏi màn hình.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            timeout: Thời gian tối đa đợi (giây)
            interval: Khoảng thời gian giữa các lần tìm kiếm (giây)
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            
        Returns:
            True nếu hình ảnh biến mất trong thời gian chờ, False nếu không
        """
        logger.debug(f"Đợi hình ảnh biến mất: {template_path}")
        return self.image_recognition.wait_until_image_disappears(
            template_path=template_path,
            timeout=timeout,
            interval=interval,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
    
    def is_image_present(self, template_path: str, threshold: float = 0.8,
                        region: Optional[Tuple[int, int, int, int]] = None,
                        scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                        use_gray: bool = True, use_canny: bool = False) -> bool:
        """
        Kiểm tra xem hình ảnh có xuất hiện trên màn hình không.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            
        Returns:
            True nếu hình ảnh xuất hiện, False nếu không
        """
        logger.debug(f"Kiểm tra hình ảnh có xuất hiện: {template_path}")
        return self.image_recognition.is_image_present(
            template_path=template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
    
    def swipe_between_images(self, start_template_path: str, end_template_path: str, 
                            duration: int = 500, threshold: float = 0.8,
                            region: Optional[Tuple[int, int, int, int]] = None,
                            scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                            use_gray: bool = True, use_canny: bool = False,
                            start_offset: Tuple[int, int] = (0, 0),
                            end_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Thực hiện thao tác vuốt từ vị trí hình ảnh đầu tiên đến vị trí hình ảnh thứ hai.
        
        Args:
            start_template_path: Đường dẫn đến hình ảnh mẫu bắt đầu
            end_template_path: Đường dẫn đến hình ảnh mẫu kết thúc
            duration: Thời gian vuốt (ms)
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            start_offset: Độ lệch (dx, dy) cho điểm bắt đầu
            end_offset: Độ lệch (dx, dy) cho điểm kết thúc
            
        Returns:
            True nếu thao tác thành công, False nếu không
        """
        # Tìm vị trí hình ảnh bắt đầu
        start_result = self.find_image(
            template_path=start_template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
        
        # Tìm vị trí hình ảnh kết thúc
        end_result = self.find_image(
            template_path=end_template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
        
        # Nếu tìm thấy cả hai hình ảnh
        if start_result and end_result:
            start_x, start_y, _ = start_result
            end_x, end_y, _ = end_result
            
            # Áp dụng độ lệch
            start_x += start_offset[0]
            start_y += start_offset[1]
            end_x += end_offset[0]
            end_y += end_offset[1]
            
            # Thực hiện vuốt
            logger.debug(f"Vuốt từ ({start_x}, {start_y}) đến ({end_x}, {end_y})")
            self.adb.run(f"shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}")
            return True
        
        return False
    
    def long_press_image(self, template_path: str, duration: int = 1000, threshold: float = 0.8,
                        region: Optional[Tuple[int, int, int, int]] = None,
                        scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                        use_gray: bool = True, use_canny: bool = False,
                        press_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Tìm hình ảnh trên màn hình và thực hiện nhấn giữ tại vị trí đó.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            duration: Thời gian nhấn giữ (ms)
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            press_offset: Độ lệch (dx, dy) khi nhấn giữ so với tâm hình ảnh
            
        Returns:
            True nếu tìm thấy và nhấn giữ thành công, False nếu không
        """
        result = self.find_image(
            template_path=template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
        
        if result:
            x, y, _ = result
            # Áp dụng độ lệch
            x += press_offset[0]
            y += press_offset[1]
            
            # Thực hiện nhấn giữ (swipe tại chỗ)
            logger.debug(f"Nhấn giữ tại ({x}, {y}) trong {duration}ms")
            self.adb.run(f"shell input swipe {x} {y} {x} {y} {duration}")
            return True
        
        return False
    
    def double_tap_image(self, template_path: str, threshold: float = 0.8,
                        region: Optional[Tuple[int, int, int, int]] = None,
                        scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                        use_gray: bool = True, use_canny: bool = False,
                        tap_offset: Tuple[int, int] = (0, 0),
                        tap_delay: float = 0.1) -> bool:
        """
        Tìm hình ảnh trên màn hình và thực hiện nhấp đúp vào vị trí đó.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            tap_offset: Độ lệch (dx, dy) khi nhấp chuột so với tâm hình ảnh
            tap_delay: Thời gian chờ giữa hai lần nhấp (giây)
            
        Returns:
            True nếu tìm thấy và nhấp đúp thành công, False nếu không
        """
        import time
        
        result = self.find_image(
            template_path=template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
        
        if result:
            x, y, _ = result
            # Áp dụng độ lệch
            x += tap_offset[0]
            y += tap_offset[1]
            
            # Thực hiện nhấp đúp
            logger.debug(f"Nhấp đúp tại ({x}, {y})")
            self.adb.run(f"shell input tap {x} {y}")
            time.sleep(tap_delay)
            self.adb.run(f"shell input tap {x} {y}")
            return True
        
        return False
    
    def drag_image_to_position(self, template_path: str, target_x: int, target_y: int, 
                              duration: int = 500, threshold: float = 0.8,
                              region: Optional[Tuple[int, int, int, int]] = None,
                              scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                              use_gray: bool = True, use_canny: bool = False,
                              drag_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Tìm hình ảnh trên màn hình và kéo đến vị trí đích.
        
        Args:
            template_path: Đường dẫn đến hình ảnh mẫu cần tìm
            target_x: Tọa độ X đích
            target_y: Tọa độ Y đích
            duration: Thời gian kéo (ms)
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            drag_offset: Độ lệch (dx, dy) khi kéo so với tâm hình ảnh
            
        Returns:
            True nếu tìm thấy và kéo thành công, False nếu không
        """
        result = self.find_image(
            template_path=template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
        
        if result:
            x, y, _ = result
            # Áp dụng độ lệch
            x += drag_offset[0]
            y += drag_offset[1]
            
            # Thực hiện kéo
            logger.debug(f"Kéo từ ({x}, {y}) đến ({target_x}, {target_y})")
            self.adb.run(f"shell input swipe {x} {y} {target_x} {target_y} {duration}")
            return True
        
        return False
    
    def drag_image_to_image(self, source_template_path: str, target_template_path: str, 
                           duration: int = 500, threshold: float = 0.8,
                           region: Optional[Tuple[int, int, int, int]] = None,
                           scale_range: Tuple[float, float] = (0.8, 1.2), scale_steps: int = 5,
                           use_gray: bool = True, use_canny: bool = False,
                           source_offset: Tuple[int, int] = (0, 0),
                           target_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Tìm hai hình ảnh trên màn hình và kéo từ hình ảnh nguồn đến hình ảnh đích.
        
        Args:
            source_template_path: Đường dẫn đến hình ảnh mẫu nguồn
            target_template_path: Đường dẫn đến hình ảnh mẫu đích
            duration: Thời gian kéo (ms)
            threshold: Ngưỡng tương đồng (0.0 - 1.0)
            region: Vùng tìm kiếm (x, y, width, height), None = toàn màn hình
            scale_range: Phạm vi tỷ lệ để tìm kiếm (min_scale, max_scale)
            scale_steps: Số bước tỷ lệ trong phạm vi
            use_gray: Sử dụng ảnh xám để tăng tốc độ tìm kiếm
            use_canny: Sử dụng phát hiện cạnh Canny để cải thiện kết quả với hình ảnh mờ
            source_offset: Độ lệch (dx, dy) cho điểm nguồn
            target_offset: Độ lệch (dx, dy) cho điểm đích
            
        Returns:
            True nếu tìm thấy cả hai hình ảnh và kéo thành công, False nếu không
        """
        # Tìm vị trí hình ảnh nguồn
        source_result = self.find_image(
            template_path=source_template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
        
        # Tìm vị trí hình ảnh đích
        target_result = self.find_image(
            template_path=target_template_path,
            threshold=threshold,
            region=region,
            scale_range=scale_range,
            scale_steps=scale_steps,
            use_gray=use_gray,
            use_canny=use_canny
        )
        
        # Nếu tìm thấy cả hai hình ảnh
        if source_result and target_result:
            source_x, source_y, _ = source_result
            target_x, target_y, _ = target_result
            
            # Áp dụng độ lệch
            source_x += source_offset[0]
            source_y += source_offset[1]
            target_x += target_offset[0]
            target_y += target_offset[1]
            
            # Thực hiện kéo
            logger.debug(f"Kéo từ ({source_x}, {source_y}) đến ({target_x}, {target_y})")
            self.adb.run(f"shell input swipe {source_x} {source_y} {target_x} {target_y} {duration}")
            return True
        
        return False
