from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class Categoria(BaseModel):
    descricao = models.CharField(max_length=100, unique=True, verbose_name='Descrição')

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.descricao


class Status(BaseModel):
    descricao = models.CharField(max_length=50, unique=True, verbose_name='Descrição')

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.descricao


class Unidade(BaseModel):
    descricao = models.CharField(max_length=20, unique=True, verbose_name='Unidade')

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.descricao


class Motivo(BaseModel):
    descricao = models.CharField(max_length=50, unique=True, verbose_name='Descrição')

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Motivo'
        verbose_name_plural = 'Motivos'

    def __str__(self):
        return self.descricao


class Funcao(BaseModel):
    descricao = models.CharField(max_length=50, unique=True, verbose_name='Descrição')

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'

    def __str__(self):
        return self.descricao


class Colaborador(BaseModel):
    nome = models.CharField(max_length=150, unique=True, verbose_name='Nome')

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Status'
    )

    funcao = models.ForeignKey(
        Funcao,
        on_delete=models.PROTECT,
        null=True,        # ⭐ Evita erro em migração futura
        blank=True,
        verbose_name='Função'
    )

    class Meta:
        ordering = ['nome']
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'

    def __str__(self):
        return self.nome


class Fornecedor(BaseModel):
    nome = models.CharField(max_length=150, unique=True, verbose_name='Nome Fornecedor')

    cnpj_cpf = models.CharField(max_length=20, unique=True, verbose_name='CNPJ / CPF')

    endereco = models.TextField(null=True, blank=True, verbose_name='Endereço')

    contato = models.CharField(max_length=100, null=True, blank=True, verbose_name='Contato')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    def __str__(self):
        return self.nome


class CentroCusto(BaseModel):
    descricao = models.CharField(max_length=100, unique=True, verbose_name='Descrição')

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'

    def __str__(self):
        return self.descricao


class NotaFiscal(BaseModel):
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Fornecedor'
    )

    arquivo = models.FileField(
        upload_to='notas_fiscais/',
        null=True,
        blank=True,
        verbose_name='Arquivo (PDF/XML)'
    )

    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'

    def __str__(self):
        return f"NF {self.id}"


class Produto(BaseModel):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)

    minimo_produto = models.PositiveIntegerField(default=0, verbose_name='Estoque Mínimo')

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.descricao


class Movimentacao(BaseModel):
    TIPO_MOV = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
        ('D', 'Devolução'),
    )

    tipo_mov = models.CharField(max_length=1, choices=TIPO_MOV)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    motivo = models.ForeignKey(   
        Motivo,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.PROTECT)

    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT)

    quantidade_mov = models.IntegerField(verbose_name='Quantidade')

    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    arquivo = models.ImageField(
        upload_to='foto_produto/',
        null=True,
        blank=True
    )

    observacao_mov = models.TextField(null=True, blank=True)

    data_mov = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-data_mov']
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'

    def clean(self):
        if self.tipo_mov in ['S', 'D']:
            self.fornecedor = None
            self.nota_fiscal = None

    def __str__(self):
        return f"{self.get_tipo_mov_display()} - {self.produto}"
