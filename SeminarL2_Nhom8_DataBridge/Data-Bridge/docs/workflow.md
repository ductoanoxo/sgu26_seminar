Viewed AGENTS.md:1-6

Để minh họa cụ thể, giả sử bạn muốn sửa một lỗi: **"Nút Login trên thanh điều hướng (NavBar) bị mất hiệu ứng mờ (blur) khi cuộn trang trên trình duyệt Safari"**.

Dưới đây là quy trình 4 bước phối hợp với AI:

### Bước 1: Gửi yêu cầu kèm Context (Luật)
Bạn không chỉ nói "sửa lỗi blur", mà hãy nhắc AI về các tiêu chuẩn đã đặt ra:
> **Bạn:** *"Nút Login đang bị mất hiệu ứng blur trên Safari. Hãy đọc `@frontend/AGENTS.md` để nắm quy ước UI và `@.agents/AGENTS.md` để đảm bảo dùng đúng chuẩn Next.js. Chú ý giữ phong cách Glassmorphism cao cấp nhé."*

### Bước 2: AI phân tích và đối chiếu
Lúc này, AI sẽ thực hiện các hành động ngầm:
1.  **Đọc luật tổng:** Biết rằng dự án dùng Next.js App Router và Tailwind/CSS Variables.
2.  **Đọc luật riêng:** Thấy quy định về việc ưu tiên dùng các biến CSS thay vì fix cứng mã màu.
3.  **Kiểm tra code hiện tại:** Phát hiện ra thuộc tính `backdrop-filter` cần có prefix `-webkit-` để chạy được trên Safari.

### Bước 3: Thực hiện sửa lỗi (Code)
AI sẽ đề xuất thay đổi trong `globals.css` hoặc component tương ứng:
```css
/* AI sẽ viết code dựa trên luật Glassmorphism bạn đã đặt ra */
.hero-btn-login {
  background: rgba(255, 255, 255, 0.1);
  -webkit-backdrop-filter: blur(8px); /* Thêm prefix cho Safari theo luật Premium UI */
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  /* ... các thuộc tính khác ... */
}
```

### Bước 4: Kiểm chứng và Báo cáo (Verification)
Sau khi sửa xong, AI sẽ phản hồi lại bạn kèm theo xác nhận đã tuân thủ luật:
> **AI:** *"Tôi đã bổ sung prefix `-webkit-backdrop-filter` để fix lỗi trên Safari. 
> - **Đối chiếu luật:** Đã đảm bảo giữ đúng style Glassmorphism theo `@frontend/AGENTS.md`.
> - **Testing:** Theo `@.agents/AGENTS.md`, bạn nên chạy lệnh `npm run dev` để kiểm tra lại trên trình duyệt trước khi commit."*

---

### Mẹo nhỏ cho bạn:
Nếu bạn thấy file `frontend/AGENTS.md` hiện tại còn quá đơn sơ (chỉ có luật về Next.js), bạn có thể yêu cầu AI: 
*"Hãy dựa vào những gì chúng ta đã thống nhất về giao diện (Glassmorphism, font Fustat, màu nền tối), hãy cập nhật thêm các quy ước UI/UX vào `@frontend/AGENTS.md` để các lần sau không cần nhắc lại nữa."*

**Kết quả:** Những lần sau, ngay cả khi bạn quên nhắc về "Glassmorphism", AI chỉ cần đọc file Agent là sẽ tự động viết code theo phong cách đó!_
