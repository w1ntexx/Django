menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
]


class DataMixin:
    paginate_by = 5
    title_page = None
    spec_selected = None
    extra_context = {}
    
    
    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page
            
        if self.spec_selected is not None:
            self.extra_context["spec_selected"] = self.spec_selected
            
    
    def get_mixin_context(self, context, select=None, **kwargs):
        context["spec_selected"] = select
        context.update(kwargs)
        return context