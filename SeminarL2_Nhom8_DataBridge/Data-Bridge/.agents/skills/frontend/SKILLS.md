---

### Tên Skill: Kiến trúc sư UI/UX Modern SaaS (Data Bridge Style with Video Background)

**Mô tả:** 
Skill này chịu trách nhiệm xây dựng giao diện kết hợp giữa Video Background sinh động và phong cách thiết kế Modern SaaS Light-Mode (lấy cảm hứng từ Wren AI). Yêu cầu đảm bảo độ tương phản cao giữa text và video nền, sử dụng kính mờ (backdrop-blur) tinh tế.

#### 1. Quy tắc Quản lý Video Background
*   **Video Local:** Sử dụng video background local (`/bg-video.mp4`) để đảm bảo hiệu suất.
*   **Light Overlay (Rất quan trọng):** Video container phải có lớp phủ overlay cân bằng (`radial-gradient` với `rgba(255, 255, 255, 0.15)` sang `rgba(248, 250, 252, 0.7)`) kèm theo `backdrop-filter: blur(1px)`. Việc này giúp làm mờ nhẹ video nền, đảm bảo các text tối màu của Light Theme có thể đọc rõ mà không bị chìm vào video nhưng vẫn giữ được chiều sâu của video.
*   Video luôn phải set `width: 100%`, `height: 100%`, căn giữa theo chiều ngang và anchor tại center (`object-position: center`, `object-fit: cover`).

#### 2. Hệ thống Typography Cốt lõi (Data Bridge Light Theme)
*   **Font Families:** Ưu tiên sử dụng Inter hoặc Plus Jakarta Sans.
*   **Màu sắc Text:** Tiêu đề (Headline) sử dụng màu dark slate (`#0f172a`), Subtitle sử dụng màu xám (`#475569`).
*   **Tracking & Line-height:** 
    *   Headline: Font size lớn (64px+), font-weight siêu đậm (800), tracking âm (`letter-spacing: -2px`) và `line-height: 1.1`.
    *   Logo/Brand: Kèm SVG Icon mảnh và text "Data Bridge".

#### 3. Quy tắc Layout & Khoảng cách
*   **Floating Navbar:** Thanh điều hướng không kéo dài toàn màn hình (full-width) mà là dạng **Floating Pill** (bo tròn `9999px`), có nền trắng kính mờ `rgba(255, 255, 255, 0.85)` và bóng đổ cực nhẹ.
*   **Bố cục Hero Content:** Căn giữa, giới hạn `max-width: 900px`. Các thẻ Badge (Huy hiệu) dùng nền xanh nhạt (`#eff6ff`), chữ xanh đậm (`#1e40af`).

#### 4. Quy tắc UI/UX & Component (Search Box)
*   **Search Input Complex:** 
    *   Là một khối hộp (card) nổi bật trên nền video. 
    *   Nền trắng (`#ffffff`), góc bo lớn (`24px`), border mảnh (`#e2e8f0`).
    *   Bóng đổ: Sử dụng shadow rộng và mềm mại `0 20px 40px -12px rgba(0, 0, 0, 0.08)` để tách biệt khỏi video background.
*   **Sử dụng Icon (Minimalist):** Sử dụng các SVG icon có nét mảnh (giống Lucide Icons) để tạo cảm giác chuyên nghiệp: Icon AI Sparkle, Mũi tên lên (Send), Kẹp ghim (Attach).
*   **Hệ thống Nút bấm:**
    *   *Primary Action:* Nút bấm chính (Submit, Login) sử dụng gradient màu xanh dương nổi bật (`#2563eb` tới `#4f46e5`).
    *   *Secondary Action:* Nút xám nhạt (`#f8fafc`), text slate, bo tròn 9999px.

#### 5. Cấu trúc Component
Mọi file code phải tuân thủ phân tách:
1.  `<VideoBackground/>` (Chứa thẻ video local `bg-video.mp4` và không chứa overlay, overlay nằm ở CSS `.hero-video-container::after`).
2.  `<NavBar/>` (Chứa Floating Pill layout).
3.  `<HeroSearchInput/>` (Chứa ô nhập liệu nền trắng, bo góc 24px).
4.  Các trang chính (`page.tsx`) wrap các thành phần này trong `.hero-content-wrapper` để nằm đè lên video (z-index cao).
