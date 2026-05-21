
---

### Tên Skill: Kiến trúc sư UI/UX Modern SaaS (Modern SaaS UI/UX Architect)

**Mô tả:** 
Skill này chuyên chịu trách nhiệm xây dựng các component giao diện mang phong cách SaaS hiện đại (ưu tiên light-mode, kết hợp glassmorphism). Yêu cầu độ chính xác pixel-perfect về khoảng cách, tuân thủ nghiêm ngặt hệ thống typography và sử dụng JavaScript thuần túy cho các luồng animation phức tạp thay vì CSS transitions.

#### 1. Quy tắc Quản lý Video & Animation (Strict JS Constraints)
*   **Không sử dụng CSS Transitions cho luồng Play/Loop:** Mọi hiệu ứng mờ (fade) của video background **bắt buộc** phải dùng `requestAnimationFrame` qua JavaScript.
*   **Logic Fade-in:** Kích hoạt quá trình fade-in kéo dài 250ms ngay khi tải xong hoặc khi bắt đầu vòng lặp mới.
*   **Logic Fade-out:** Lắng nghe sự kiện `timeUpdate`. Khi video còn đúng `0.55s`, kích hoạt fade-out kéo dài 250ms.
*   **Quản lý State & Tránh xung đột:** 
    *   Sử dụng biến `fadingOutRef` (boolean) để chặn việc gọi lại fade-out nhiều lần từ `timeUpdate`.
    *   Mỗi khi một hiệu ứng fade mới bắt đầu, **phải** cancel toàn bộ animation frames đang chạy trước đó.
    *   Hiệu ứng fade phải tiếp nối từ `opacity` hiện tại (không được giật cục - no snapping).
*   **Logic Reset Loop:** Khi sự kiện `ended` kích hoạt -> set opacity = 0 -> delay 100ms -> set `currentTime = 0` -> play() -> gọi hàm fade-in.
*   **Định dạng Background:** Video luôn phải set `width: 115%`, `height: 115%`, căn giữa theo chiều ngang và anchor tại top (`object-position: top`).

#### 2. Hệ thống Typography Cốt lõi
Mọi text trong component phải được map chính xác với hệ thống font sau. Không sử dụng font mặc định nếu không có khai báo.
*   **Font Families:** Cần import đầy đủ Schibsted Grotesk, Inter, Noto Sans, Fustat (Weights: 400, 500, 600, 700).
*   **Tracking & Line-height (Rất quan trọng):** 
    *   Headline (Fustat Bold 80px) bắt buộc đi kèm tracking âm (`letter-spacing: -4.8px`) và `line-height: none` (hoặc `1`).
    *   Logo/Brand (Schibsted Grotesk SemiBold 24px) đi kèm `letter-spacing: -1.44px`.
    *   Subtitle (Fustat Medium 20px) đi kèm `letter-spacing: -0.4px`.

#### 3. Quy tắc Layout & Khoảng cách (Pixel-Perfect Spacing)
*   **Padding tổng:** Luôn giữ `120px` horizontal padding cho các layout full-width (Navbar, Hero Container). Vertical padding của Navbar luôn là `16px`.
*   **Spacing Hierarchy (Khoảng cách phân cấp):**
    *   Gap giữa Navbar và Hero Content: `60px`.
    *   Gap giữa Header Text và Input Box: `44px`.
    *   Gap nội bộ (giữa Badge -> Title -> Subtitle): `34px`.
*   **Bố cục đặc biệt:** Chấp nhận sử dụng negative margin (ví dụ: `-mt-[50px]`) để đẩy khối Hero Content lên trên, tạo sự cân bằng thị giác với Video Background.

#### 4. Quy tắc UI/UX & Tương tác (SaaS Aesthetics)
*   **Hiệu ứng Glassmorphism:** Các panel nổi (như Search Input Box) phải có `backdrop-blur` kết hợp với nền tối trong suốt (ví dụ: `rgba(0,0,0,0.24)`) để tách biệt khỏi nền video.
*   **Hệ thống Nút bấm (Button System):**
    *   *Primary Action:* Nền đen, chữ trắng (VD: nút "Log In" 101px, nút Submit hình tròn 36px).
    *   *Secondary Action:* Nền trong suốt hoặc xám nhạt (`#f8f8f8`), bo góc nhỏ (6px).
    *   *Highlight Action:* Nút nâng cấp/mua credits phải dùng màu nhấn (VD: Xanh lá `rgba(90,225,76,0.89)`).
*   **Trạng thái Input:** Vùng nhập liệu chính phải có nền trắng hoàn toàn (`#ffffff`), bo góc `12px`, có shadow đổ nhẹ, chữ placeholder màu `rgba(0,0,0,0.6)` size 16px.

#### 5. Cấu trúc Component
Mọi file code (React/Vue/HTML) đều phải chia tách rạch ròi theo cấu trúc:
1.  `<VideoBackground/>` (Chứa toàn bộ logic JS `requestAnimationFrame` và thẻ `<video>`).
2.  `<NavigationBar/>` (Layout ngang, flex-between, chứa Logo và các Action buttons).
3.  `<HeroContent/>` (Căn giữa, giới hạn `max-width`).
    *   `<Badge/>`
    *   `<HeadlineGroup/>` (Title + Subtitle)
    *   `<SearchInputComplex/>` (Component chứa UI 2 tầng: Top row info, Main input, Bottom row actions).

