from fastapi import APIRouter, Depends

from app.dependencies.permission_dependency import require_feature
from app.models.user import User


router = APIRouter(
    prefix="/api/feature-usage",
    tags=["Feature Usage"]
)


@router.post("/generate-image")
def generate_image(
    current_user: User = Depends(require_feature("generate_image"))
):
    """
    API giả lập tính năng Generate Image.

    Chỉ user đã unlock feature generate_image mới gọi được.

    Ví dụ:
    - User mua Basic có generate_image
    - User chưa mua gói nào sẽ bị 403
    """

    return {
        "message": "Generate image feature is running",
        "user": current_user.email,
        "result": {
            "image_url": "https://example.com/fake-generated-image.png",
            "prompt": "A SaaS dashboard with credit packages"
        }
    }


@router.post("/auto-post")
def auto_post(
    current_user: User = Depends(require_feature("auto_post"))
):
    """
    API giả lập tính năng Auto Post.

    Chỉ user đã unlock feature auto_post mới gọi được.

    Ví dụ:
    - User mua Pro sẽ có auto_post
    - User chỉ mua Basic sẽ bị 403
    """

    return {
        "message": "Auto post feature is running",
        "user": current_user.email,
        "result": {
            "post_id": 1001,
            "status": "published",
            "content": "This is a fake auto-published post."
        }
    }


@router.post("/advanced-analytics")
def advanced_analytics(
    current_user: User = Depends(require_feature("advanced_analytics"))
):
    """
    API giả lập tính năng Advanced Analytics.

    Chỉ user đã unlock feature advanced_analytics mới gọi được.

    Ví dụ:
    - User mua Enterprise sẽ có advanced_analytics
    - User mua Basic/Pro sẽ bị 403
    """

    return {
        "message": "Advanced analytics feature is running",
        "user": current_user.email,
        "result": {
            "total_posts": 120,
            "total_images": 45,
            "engagement_rate": "8.5%"
        }
    }