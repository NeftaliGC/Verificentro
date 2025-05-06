const tipo_pago = document.getElementById("tipo-pago-select");
const pago = document.getElementById("pago-select");
const tit = document.getElementById("info-pago");

tipo_pago.addEventListener("change", function () {

    if (pago.value != "") {
        tit.scrollIntoView({ behavior: "smooth" });
    }

    // Ocultar todos los elementos de pago
    const allPaymentElements = document.querySelectorAll("[id^='efectivo'], [id='tarjeta']");
    allPaymentElements.forEach(element => {
        element.style.display = "none";
    });

    // Mostrar el elemento correspondiente según el valor seleccionado
    const selectedPaymentElement = document.getElementById(tipo_pago.value);
    if (selectedPaymentElement) {
        selectedPaymentElement.style.display = "block";
    }
});

