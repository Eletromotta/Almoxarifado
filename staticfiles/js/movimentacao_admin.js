console.log("JS CARREGADO DA STATIC");


document.addEventListener("DOMContentLoaded", function () {

    function getRow(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return null;
        return field.closest(".form-group") || field.closest(".form-row");
    }

    function hideRow(row) {
        row?.style.setProperty("display", "none", "important");
    }

    function showRow(row) {
        row?.style.removeProperty("display");
    }

    function toggleFields() {

        const tipoMov = document.getElementById("id_tipo_mov");
        if (!tipoMov) return;

        const fornecedorRow = getRow("id_fornecedor");
        const notaRow = getRow("id_nota_fiscal");
        const valorRow = getRow("id_valor_unitario");

        const motivoRow = getRow("id_motivo");
        const centroCustoRow = getRow("id_centro_custo");
        const colaboradorRow = getRow("id_colaborador");

        // 🔥 Mostra todos antes de aplicar regras
        [
            fornecedorRow,
            notaRow,
            valorRow,
            motivoRow,
            centroCustoRow,
            colaboradorRow
        ].forEach(showRow);

        const tipo = tipoMov.value;

        // ✅ SAÍDA
        if (tipo === "S") {
            hideRow(fornecedorRow);
            hideRow(notaRow);
            hideRow(valorRow);
            hideRow(motivoRow); // <-- ADICIONADO
        }

        // ✅ ENTRADA
        if (tipo === "E") {
            hideRow(motivoRow);
            hideRow(centroCustoRow);
            hideRow(colaboradorRow);
        }

        // ✅ DEVOLUÇÃO
        if (tipo === "D") {
            hideRow(notaRow);
            hideRow(motivoRow);
            hideRow(valorRow);
            hideRow(fornecedorRow);
        }
    }

    document.addEventListener("change", function (e) {
        if (e.target.id === "id_tipo_mov") {
            toggleFields();
        }
    });

    if (window.jQuery) {
        jQuery("#id_tipo_mov").on("select2:select", function () {
            toggleFields();
        });
    }

    toggleFields();
});
