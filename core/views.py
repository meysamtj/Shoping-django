from django.shortcuts import render
from django.views import View

"""
برای نمایش کل محصولات صفحه اصلی و محصولات بیشترین فروخته شده و جدید ترین محصولات و محصولاتی که تخفیف دارند
نمایش کتگوری ها
 و سرچ محصولات و
 و اضافه کردن به سبد خرید
"""
class Home(View):
    template_name = "core/home.html"

    def get(self, request):
        return render(request, self.template_name)
