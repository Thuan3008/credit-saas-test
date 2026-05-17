# Credit SaaS Test Assignment

Đây là project bài test Web Developer, xây dựng module mua các gói credits cho một hệ thống SaaS.

Hệ thống cho phép user xem và mua các gói credits. Sau khi thanh toán giả lập thành công, credits sẽ được cộng vào tài khoản user và các tính năng tương ứng của gói sẽ được mở khóa. Các API sử dụng tính năng sẽ được bảo vệ bằng middleware kiểm tra quyền.

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Docker

### Frontend

- ReactJS
- Vite
- React Router
- Axios
- Tailwind CSS

### Database

- PostgreSQL

---

## Chức năng chính

### Xác thực người dùng

- Đăng ký tài khoản
- Đăng nhập
- Xác thực bằng JWT
- Phân quyền theo role: user/admin

### Quản lý gói credits

- Admin có thể tạo, cập nhật, xóa và xem danh sách packages
- User có thể xem các packages đang hoạt động
- Mỗi package bao gồm:
  - tên gói
  - mô tả
  - giá
  - số credits
  - danh sách tính năng đi kèm

### Mua credits

- User có thể mua package
- Thanh toán được giả lập
- Credits được cộng vào tài khoản user sau khi mua thành công
- Lịch sử giao dịch được lưu lại

### Phân quyền tính năng

- Khi user mua package, các features tương ứng sẽ được mở khóa
- Các API sử dụng feature sẽ kiểm tra quyền trước khi cho phép truy cập
- Các feature demo:
  - Generate Image
  - Auto Post
  - Advanced Analytics

### Giao diện Frontend

- Login/Register
- Dashboard
- Hiển thị số credits hiện tại
- Hiển thị features đã mở khóa
- Trang mua package
- Trang lịch sử mua credits
- Trang admin quản lý package và feature

---

## Cấu trúc project

```
credit-saas-test/
├── backend/
│   ├── app/
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
└── README.md
```

---

## Hướng dẫn chạy project

### 1. Clone repository

```
git clone https://github.com/Thuan3008/credit-saas-test
cd credit-saas-test
```

### 2. Chạy project bằng Docker Compose

```
docker-compose up --build
```

Sau khi chạy thành công, truy cập:

```
Frontend: http://localhost:5173
Backend API Docs: http://localhost:8000/docs
PostgreSQL: localhost:5432
```

---

## Tạo dữ liệu demo

Mở Swagger:

```
http://localhost:8000/docs
```

Chạy API:

```
POST /api/seed/demo
```

API này sẽ tạo sẵn:

### Demo Admin

```
email: admin@example.com
password: 123456
```

### Demo User

```
email: user@example.com
password: 123456
```

### Demo Features

```
generate_image
auto_post
advanced_analytics
```

### Demo Packages

```
Basic
Pro
Enterprise
```

---

## Luồng demo

### Luồng User

1. Mở frontend:

```
http://localhost:5173
```

2. Đăng nhập bằng tài khoản user:

```
email: user@example.com
password: 123456
```

3. Vào trang Packages.
4. Mua gói Basic.
5. Vào trang Dashboard.
6. Kiểm tra số credits hiện tại và các features đã mở khóa.
7. Thử sử dụng tính năng Generate Image.
8. Mua gói Pro.
9. Thử sử dụng tính năng Auto Post.
10. Vào trang Purchase History để xem lịch sử mua credits.

### Luồng Admin

1. Đăng nhập bằng tài khoản admin:

```
email: admin@example.com
password: 123456
```

2. Vào trang Admin.
3. Tạo features.
4. Tạo packages.
5. Soft delete package nếu cần.

---

## Danh sách API chính

### Auth

| Method | Endpoint             | Mô tả                       |
| ------ | -------------------- | --------------------------- |
| POST   | `/api/auth/register` | Đăng ký user                |
| POST   | `/api/auth/login`    | Đăng nhập                   |
| GET    | `/api/auth/me`       | Lấy thông tin user hiện tại |

### Features

| Method | Endpoint                     | Mô tả                      |
| ------ | ---------------------------- | -------------------------- |
| GET    | `/api/features`              | Lấy danh sách features     |
| POST   | `/api/features`              | Tạo feature, chỉ admin     |
| PUT    | `/api/features/{feature_id}` | Cập nhật feature, chỉ admin |
| DELETE | `/api/features/{feature_id}` | Xóa feature, chỉ admin     |

### Packages

| Method | Endpoint                     | Mô tả                                 |
| ------ | ---------------------------- | ------------------------------------- |
| GET    | `/api/packages`              | Lấy danh sách packages đang hoạt động |
| GET    | `/api/packages/admin`        | Lấy toàn bộ packages, chỉ admin       |
| GET    | `/api/packages/{package_id}` | Lấy chi tiết package                  |
| POST   | `/api/packages`              | Tạo package, chỉ admin                |
| PUT    | `/api/packages/{package_id}` | Cập nhật package, chỉ admin           |
| DELETE | `/api/packages/{package_id}` | Soft delete package, chỉ admin        |

### Purchases

| Method | Endpoint                      | Mô tả                  |
| ------ | ----------------------------- | ---------------------- |
| POST   | `/api/purchases/{package_id}` | Mua package            |
| GET    | `/api/purchases/history`      | Xem lịch sử mua credits |

### Users

| Method | Endpoint                 | Mô tả                            |
| ------ | ------------------------ | -------------------------------- |
| GET    | `/api/users/me/credits`  | Xem số credits hiện tại          |
| GET    | `/api/users/me/features` | Xem các features đã được mở khóa |

### Feature Usage

| Method | Endpoint                                | Mô tả                                       |
| ------ | --------------------------------------- | ------------------------------------------- |
| POST   | `/api/feature-usage/generate-image`     | API demo tính năng Generate Image có bảo vệ |
| POST   | `/api/feature-usage/auto-post`          | API demo tính năng Auto Post có bảo vệ      |
| POST   | `/api/feature-usage/advanced-analytics` | API demo tính năng Advanced Analytics có bảo vệ |

---

## Các trường hợp test phân quyền

### Khi user chưa mua package nào

Gọi API:

```
POST /api/feature-usage/generate-image
```

Kết quả mong muốn:

```
403 Forbidden
```

### Sau khi mua Basic

Feature được mở khóa:

```
generate_image
```

Được phép gọi:

```
POST /api/feature-usage/generate-image
```

Chưa được phép gọi:

```
POST /api/feature-usage/auto-post
```

### Sau khi mua Pro

Features được mở khóa:

```
generate_image
auto_post
```

Được phép gọi:

```
POST /api/feature-usage/auto-post
```

### Sau khi mua Enterprise

Features được mở khóa:

```
generate_image
auto_post
advanced_analytics
```

Được phép gọi:

```
POST /api/feature-usage/advanced-analytics
```

---

## Ghi chú

- Project sử dụng thanh toán giả lập, không tích hợp cổng thanh toán thật.
- Package khi xóa sẽ dùng soft delete bằng cách set `is_active = false`.
- Frontend lưu JWT token trong localStorage.
- Database tables được tạo tự động khi backend start bằng SQLAlchemy `create_all`.
- Swagger API Docs có sẵn tại `http://localhost:8000/docs`.

---

## Lưu ý khi test API bằng Swagger

Một số API yêu cầu user phải đăng nhập trước, ví dụ:

- `GET /api/auth/me`
- `POST /api/purchases/{package_id}`
- `GET /api/purchases/history`
- `GET /api/users/me/credits`
- `GET /api/users/me/features`
- `POST /api/features`
- `POST /api/packages`
- `POST /api/feature-usage/generate-image`

Cách đăng nhập và gắn token trong Swagger:

Gọi API đăng nhập

```txt
POST /api/auth/login
    Body: 
        {
             "email": "user@example.com",
             "password": "123456"
        }
    API sẽ trả về: 
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user": {
            "id": 1,
            "email": "user@example.com",
            "full_name": "Normal User",
            "role": "user"
                    }
        }

Copy access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Bấm nút "Authorize" phía trên bên phải của Swagger và dán token vào