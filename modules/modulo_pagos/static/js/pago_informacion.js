const tipo_pago = document.getElementById("tipo-pago-select");
const pago = document.getElementById("pago-select");
const tit = document.getElementById("info-pago");

tipo_pago.addEventListener("change", function () {

    if (pago.value != "") {
        tit.scrollIntoView({ behavior: "smooth" });
    }

    if (tipo_pago.value == "efectivo_verificentro") {

        document.getElementById("efectivo_verificentro").style.display = "block";
        document.getElementById("efectivo_banco").style.display = "none";
        document.getElementById("tarjeta").style.display = "none";

    } else if (tipo_pago.value == "efectivo_banco") {

        document.getElementById("efectivo_banco").style.display = "block";
        document.getElementById("efectivo_verificentro").style.display = "none";
        document.getElementById("tarjeta").style.display = "none";

    } else if (tipo_pago.value == "tarjeta") {

        document.getElementById("tarjeta").style.display = "block";
        document.getElementById("efectivo_verificentro").style.display = "none";
        document.getElementById("efectivo_banco").style.display = "none";

    } else {
        document.getElementById("efectivo_verificentro").style.display = "none";
        document.getElementById("efectivo_banco").style.display = "none";
        document.getElementById("tarjeta").style.display = "none";
    }
});