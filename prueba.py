from src.services.usuario_service import Usuario_service
from src.persistence.json_functions import JsonFunctions
if __name__=="__main__":

    data =JsonFunctions("data/usuarios.json")
    data.get_all()
    usuario_service =Usuario_service()
    #["administrador", "socio", "no_socio"]
    usuarioadmin={
        "Nombre":"admin",

        "Apellido":"",

        "TipodeUsuario":"administrador",

        "Dirección":"",

        "Teléfono":"",

        "NumSocio":"Ad"
    }
    usuarioAnonimo={
        "Nombre":"anonimo",

        "Apellido":"",

        "TipodeUsuario":"no_socio",

        "Dirección":"",

        "Teléfono":"",

        "NumSocio":"An"
    }

    usuario={
        "Nombre":"ruben",

        "Apellido":"cano",

        "TipodeUsuario":"socio",

        "Dirección":"madrid",

        "Teléfono":"664664664",

        "NumSocio":"S01"
    }
    usuario_service.crearUsuario(usuarioadmin)
    usuario_service.crearUsuario(usuarioAnonimo)
    usuario_service.crearUsuario(usuario)
