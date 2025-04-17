import * as crypto from "crypto";

class Transaccion {
    constructor(
        public cantidad: number,
        public pagador: string,
        public recibidor: string,
    ) {}
    toString(){
        return JSON.stringify(this)
    }
}

class Bloque {

    public numeroAleatorio = Math.random() * 999999999;
    constructor(
        public hashAnterior: string,
        public transaccion: Transaccion,
        public momento = Date.now()
    ){}

    get hash() {
        const str = JSON.stringify(this);
        const hash = crypto.createHash("SHA256");
        hash.update(str).end();
        return hash.digest("hex")
    }
}



class Cadena {
    public static instancia = new Cadena();
    cadena: Bloque[]

    constructor(){
        this.cadena = [new Bloque(null, new Transaccion(100, "EJ_PAGADOR", "EJ_RECIBIDOR"))]
    }

    get ultimoBloque() {
        return this.cadena[this.cadena.length - 1]
    }

    minar(numeroAleatorio:number) {
        let solucion = 1;
        console.log("MINANDO AHORA...");
        while(true) {
            const hash = crypto.createHash("MD5");
            hash.update((numeroAleatorio + solucion).toString()).end()

            const intento = hash.digest("hex");
            if intento.substr(0,4) === "0000" {
                console.log("RESUELTO: ${solucion}");
                return solucion;
            }
        }
    }

    crearBloque(transaccion: Transaccion, claveDeEnvio: string, firma: string) {
    const verificador = crypto.createVerify("SHA256");
    verificador.update(transaccion.toString());

    const validez = verificador.verify(claveDeEnvio, firma)
    if (validez){
        const bloqueNuevo = new Bloque(this.ultimoBloque.hash, transaccion);
        this.minar(bloqueNuevo.numeroAleatorio)
        this.cadena.push()
    }
}}


class Cartera {
        public clavePublica: string; //para recibir dinero
        public clavePrivada: string; //para enviar dinero

    constructor(){
        const claveDeEmparejamiento = crypto.generateKeyPairSync("rsa", {
            modulusLength: 2048,
            clavePublicaCifrada: {type: "spki", format: "pem"},
            clavePrivadaCifrada: {type: "pkcs8", format: "pem"},
        });

        this.clavePrivada = claveDeEmparejamiento.privateKey;
        this.clavePublica = claveDeEmparejamiento.publicKey;
    }

    enviarDinero(cantidad:number, clavePublicaDelRecibidor: string) {
        const transaccion = new Transaccion(cantidad, this.clavePublica, clavePublicaDelRecibidor);  
        const firmar = crypto.createSign("SHA256");
        firmar.update(transaccion.toString()).end();

        const firma = firmar.sign(this.clavePrivada);
        Cadena.instancia.crearBloque(transaccion, this.clavePublica, firma)
    }
}

if (true){ //ejemplo de uso
const ejemploPersona = new Cartera();
const ejemploPersona2 = new Cartera();
ejemploPersona.enviarDinero(23, ejemploPersona.clavePublica)
ejemploPersona2.enviarDinero(46, ejemploPersona.clavePublica)

console.log(Cadena.instancia)
}