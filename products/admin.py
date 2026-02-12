from django.contrib import admin
from django.db.models import Sum, Case, When, IntegerField, F
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from datetime import date
from django.utils.formats import date_format


from .models import (
    Categoria,
    Status,
    Unidade,
    Fornecedor,
    CentroCusto,
    Produto,
    NotaFiscal,
    Movimentacao,
    Colaborador,
    Motivo,
    Funcao
)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    actions = None
    search_fields = ('descricao',)
    list_filter = ("created_at",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    actions = None
    search_fields = ('descricao',)
    list_filter = ("created_at",)

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    actions = None
    search_fields = ('descricao',)
    list_filter = ("created_at",)

@admin.register(Motivo)
class MotivoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    actions = None
    search_fields = ('descricao',)
    list_filter = ("created_at",)

@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    actions = None
    search_fields = ('descricao',)
    list_filter = ("created_at",)

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome','funcao','status')
      
@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj_cpf', 'contato')
    search_fields = ('nome', 'cnpj_cpf')

@admin.register(CentroCusto)
class CentroCustoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    actions = None
    search_fields = ('descricao',)

@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):

    list_display = ('fornecedor','arquivo', 'created_at')
    search_fields = ('created_at',)
    actions = None
    list_filter = ("created_at",)
    autocomplete_fields = (
        'fornecedor',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'categoria',
        'unidade',
        'saldo_atual',
        'minimo_produto',
        'estoque_critico',
        'status'
    )
    list_filter = ('categoria', 'status')
    search_fields = ('descricao',)
    autocomplete_fields = ('categoria', 'status', 'unidade')

    def saldo_atual(self, obj):
        saldo = Movimentacao.objects.filter(
            produto=obj
        ).aggregate(
            saldo=Sum(
                Case(
                    When(tipo_mov='E', then=F('quantidade_mov')),
                    When(tipo_mov='S', then=-F('quantidade_mov')),
                    When(tipo_mov='D', then=F('quantidade_mov')),
                    output_field=IntegerField()
                )
            )
        )['saldo'] or 0
        return saldo

    saldo_atual.short_description = 'Saldo Atual'

    # def estoque_critico(self, obj):
    #     return self.saldo_atual(obj) <= obj.minimo_produto

    # estoque_critico.boolean = True
    # estoque_critico.short_description = 'Estoque Baixo'

    def estoque_critico(self, obj):

        if self.saldo_atual(obj) <= obj.minimo_produto:
            return format_html(
                '<span style="color:{};font-weight:bold;">{}</span>',
                '#ff8c42',
                'Estoque Baixo'
            )

        return format_html(
            '<span style="color:{};font-weight:bold;">{}</span>',
            '#000000',
            'Normal'
        )


# @admin.register(Movimentacao)
# class MovimentacaoAdmin(admin.ModelAdmin):

#     list_per_page = 100
#     class Media:
#         js = ('js/movimentacao_admin.js',)

    
#     list_display = (
#         'tipo_mov',
#         'produto',
#         'motivo',
#         'quantidade_mov',
#         'centro_custo',
#         'data_mov',
#         'arquivo'
#     )
#     list_filter = ('tipo_mov', 'data_mov')
#     search_fields = ('produto__descricao',)
#     autocomplete_fields = (
#         'produto',
#         'fornecedor',
#         'nota_fiscal',
#         'centro_custo'
#     )
#     readonly_fields = ('data_mov',)

#     def has_change_permission(self, request, obj=None):
#         if obj:
#             return False
#         return super().has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         return False


# @admin.register(Movimentacao)
# class MovimentacaoAdmin(admin.ModelAdmin):

#     list_per_page = 100

#     class Media:
#         js = ('js/movimentacao_admin.js',)

#     list_display = (
#         'tipo_mov',
#         'produto',
#         'motivo',
#         'quantidade_mov',
#         'centro_custo',
#         'data_mov_formatada',   # ✅ substituí aqui
#         'arquivo'
#     )

#     list_filter = ('tipo_mov', 'data_mov')

#     search_fields = ('produto__descricao',)

#     autocomplete_fields = (
#         'produto',
#         'fornecedor',
#         'nota_fiscal',
#         'centro_custo'
#     )

#     readonly_fields = ('data_mov',)

#     # ✅ Formatação da data simplificada
#     def data_mov_formatada(self, obj):
#         return date_format(obj.data_mov, "d/m/Y H:i")

#     data_mov_formatada.short_description = "Data Mov."
#     data_mov_formatada.admin_order_field = "data_mov"

#     # ✅ Bloqueia edição
#     def has_change_permission(self, request, obj=None):
#         if obj:
#             return False
#         return super().has_change_permission(request, obj)

#     # ✅ Bloqueia exclusão
#     def has_delete_permission(self, request, obj=None):
#         return False

from django.contrib import admin
from django.utils.formats import date_format
from django.utils.html import format_html
from .models import Movimentacao


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):

    list_per_page = 100

    class Media:
        js = ('js/movimentacao_admin.js',)

    list_display = (
        'tipo_mov',
        'produto',
        'motivo',
        'quantidade_mov',
        'centro_custo',
        'data_mov_formatada',
        'preview_imagem',   # ✅ preview aqui
    )

    list_filter = (
        'tipo_mov',
        'data_mov',
    )

    search_fields = ('produto__descricao',)

    autocomplete_fields = (
        'produto',
        'fornecedor',
        'nota_fiscal',
        'centro_custo'
    )

    readonly_fields = ('data_mov',)

    # 🔹 Data compacta
    def data_mov_formatada(self, obj):
        return date_format(obj.data_mov, "d/m/Y H:i")

    data_mov_formatada.short_description = "Data Mov."
    data_mov_formatada.admin_order_field = "data_mov"

    # 🔹 Preview da imagem
    def preview_imagem(self, obj):
        if obj.arquivo:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:40px; border-radius:4px;" />'
                '</a>',
                obj.arquivo.url,
                obj.arquivo.url
            )
        return "—"

    preview_imagem.short_description = "Foto"

    # 🔒 Bloqueios
    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False
