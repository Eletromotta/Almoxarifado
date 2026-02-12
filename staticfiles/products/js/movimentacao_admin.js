document.addEventListener("DOMContentLoaded", function () {

    function toggleFields() {

        document.addEventListener('DOMContentLoaded', function () {
        console.log("DOM pronto");
        });


        const tipoMov = document.querySelector("#id_tipo_mov");

        const fornecedorRow = document.querySelector(".form-row.field-fornecedor");
        const notaRow = document.querySelector(".form-row.field-nota_fiscal");
        const valorRow = document.querySelector(".form-row.field-valor_unitario");

        if (!tipoMov) return;

        if (tipoMov.value === "S") {

            if (fornecedorRow) fornecedorRow.style.display = "none";
            if (notaRow) notaRow.style.display = "none";
            if (valorRow) valorRow.style.display = "none";

        } else {

            if (fornecedorRow) fornecedorRow.style.display = "";
            if (notaRow) notaRow.style.display = "";
            if (valorRow) valorRow.style.display = "";
        }
    }

    document.addEventListener("change", function (e) {
        if (e.target.id === "id_tipo_mov") {
            toggleFields();
        }
    });

    toggleFields();
});
