import csv
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import Sum, Case, When, IntegerField, F
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.formats import date_format
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import utils
from reportlab.lib.units import inch
import os
from django.urls import path
from django.shortcuts import redirect

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
    
    list_display = ('nome', 'funcao', 'matricula', 'area', 'status')
    actions = ['ver_movimentacoes']

    def ver_movimentacoes(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Selecione apenas um colaborador.")
            return

        colaborador = queryset.first()

        url = reverse(
            'admin:products_colaborador_movimentacoes',
            args=[colaborador.id]
        )

        return redirect(url)


    ver_movimentacoes.short_description = "Ver movimentações do colaborador"

    def movimentacoes_view(self, request, colaborador_id):

        colaborador = Colaborador.objects.get(pk=colaborador_id)

        movimentacoes = Movimentacao.objects.filter(
            colaborador=colaborador
        ).select_related('produto', 'motivo')

        context = dict(
            self.admin_site.each_context(request),
            colaborador=colaborador,
            movimentacoes=movimentacoes,
        )

        return render(request, "admin/movimentacoes_colaborador.html", context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:colaborador_id>/movimentacoes/',
                self.admin_site.admin_view(self.movimentacoes_view),
                name='products_colaborador_movimentacoes',
            ),
            path(
                '<int:colaborador_id>/movimentacoes/pdf/',
                self.admin_site.admin_view(self.exportar_pdf),
                name='products_colaborador_movimentacoes_pdf',
            ),
        ]
        return custom_urls + urls
    
    def exportar_pdf(self, request, colaborador_id):

        colaborador = Colaborador.objects.get(pk=colaborador_id)

        movimentacoes = Movimentacao.objects.filter(
            colaborador=colaborador
        ).order_by('-data_mov')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="movimentacoes_{colaborador.nome}.pdf"'

        doc = SimpleDocTemplate(response)
        elements = []

        styles = getSampleStyleSheet()

        # 🔹 LOGO DA EMPRESA
        logo_path = os.path.join('static/images', 'logo_eletromotta.jpg')  # ajuste se necessário

        if os.path.exists(logo_path):
            img = Image(logo_path, width=2*inch, height=1*inch)
            elements.append(img)

        elements.append(Spacer(1, 12))

        # 🔹 TÍTULO
        titulo = Paragraph(f"<b>Relatório de Movimentações</b><br/>{colaborador.nome}", styles['Title'])
        elements.append(titulo)

        elements.append(Spacer(1, 20))

        # 🔹 DADOS DA TABELA
        data = [
            ['Produto', 'Tipo', 'Data', 'Motivo']
        ]

        for mov in movimentacoes:
            tipo = "ENTREGA" if mov.tipo_mov == 'S' else "DEVOLUÇÃO"

            data.append([
                str(mov.produto),
                tipo,
                mov.data_mov.strftime("%d/%m/%Y %H:%M"),
                mov.motivo or ""
            ])

        table = Table(data, repeatRows=1)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 1), (-2, -1), 'CENTER'),
        ]))

        elements.append(table)

        doc.build(elements)

        return response

    #list_display = ('nome', 'funcao', 'matricula', 'area', 'status', 'created_at', 'updated_at' )

    #actions = ['export_to_csv']

    # def export_to_csv(self, request, queryset):
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="colaborador.csv"'

    #     writer = csv.writer(response)
    #     writer.writerow([
    #         'Nome',
    #         'Função',
    #         'Matrícula',
    #         'Área',
    #         'Status',
    #         'Criado em',
    #         'Atualizado em'
    #     ])

    #     for colaborador in queryset:
    #         writer.writerow([
    #             colaborador.nome,
    #             colaborador.funcao.descricao if colaborador.funcao else '',
    #             colaborador.matricula,
    #             colaborador.area if colaborador.area else '',
    #             colaborador.status if colaborador.status else '',
    #             colaborador.created_at,
    #             colaborador.updated_at
    #         ])

    #     return response

    # export_to_csv.short_description = 'Exportar selecionados para CSV'

    # actions = [export_to_csv]

      
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
