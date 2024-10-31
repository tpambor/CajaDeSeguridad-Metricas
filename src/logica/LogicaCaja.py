import random
import re
from datetime import datetime, timedelta
from typing import List

from .typing import TipoClaveFavorita, TipoElemento, TipoReporte
from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad, TIPO_IDENTIFICACION, TIPO_TARJETA, TIPO_SECRETO, TIPO_LOGIN

from src.modelo.declarative_base import engine, Base, Session
from src.modelo import Caja, ClaveFavorita, Elemento, Tarjeta, Identificacion, Login, Secreto

ERROR_NOMBRE_1 = "El nombre no debe tener menos de 1 caracter"
ERROR_NOMBRE_255 = "El nombre no debe tener más de 255 caracteres"
ERROR_CLAVE_3 = "La clave no debe tener menos de 3 caracteres"
ERROR_CLAVE_255 = "La clave no debe tener más de 255 caracteres"
ERROR_PISTA_3 = "La pista no debe tener menos de 3 caracteres"
ERROR_PISTA_255 = "La pista no debe tener más de 255 caracteres"
ERROR_ELEMENTO_EXISTENTE = "Ya existe un elemento con este nombre"
ERROR_CLAVE_UTILIZADA = "No se puede eliminar una clave utilizada"
ERROR_USUARIO_1 = "El usuario no debe tener menos de 1 caracter"
ERROR_USUARIO_255 = "El usuario no debe tener más de 255 caracteres"
ERROR_NOTAS_3 = "Las notas no deben tener menos de 3 caracteres"
ERROR_NOTAS_512 = "Las notas no deben tener más de 512 caracteres"
ERROR_FORMATO_EMAIL = "El email no tiene el formato correcto"
ERROR_URL_512 = "La URL no debe tener más de 512 caracteres"
ERROR_FORMAT_URL = "El url no tiene el formato correcto"
ERROR_ASIGNADO_CLAVE = "Debe tener asignado una clave favorita"
ERROR_SECRETO_3 = "El secreto no debe tener menos de 3 caracteres"
ERROR_SECRETO_255 = "El secreto no debe tener más de 255 caracteres"
ERROR_NOMBRE_COMPLETO_3 = "El nombre completo no debe tener menos de 3 caracteres"
ERROR_NOMBRE_COMPLETO_255 = "El nombre completo no debe tener más de 255 caracteres"
ERROR_NUMERO_DIGITOS = "El número sólo debe contener dígitos"
ERROR_NUMERO_3 = "El número no debe tener menos de 3 dígitos"
ERROR_NUMERO_20 = "El número no debe tener más de 20 dígitos"
ERROR_NUMERO_255 = "El número no debe tener más de 255 dígitos"
ERROR_TITULAR_3 = "El titular no debe tener menos de 3 caracteres"
ERROR_TITULAR_255 = "El titular no debe tener más de 255 caracteres"
ERROR_TITULAR_FORMATO = "El titular debe contener solo mayúsculas y espacios"
ERROR_FECHA_VENCIMIENTO = "La fecha de vencimiento debe tener el formato YYYY-MM-DD, por ejemplo 2023-01-28"
ERROR_FECHA_EXPEDICION = "La fecha de expedición debe tener el formato YYYY-MM-DD, por ejemplo 2023-01-28"
ERROR_FECHA_NACIMIENTO = "La fecha de nacimiento debe tener el formato YYYY-MM-DD, por ejemplo 2023-01-28"
ERROR_DIRECCION_3 = "La dirección no debe tener menos de 3 caracteres"
ERROR_DIRECCION_255 = "La dirección no debe tener más de 255 caracteres"
ERROR_TELEFONO_FORMATO = "El teléfono deber contener un número de teléfono, por ejemplo +57 (606) 7422736"
ERROR_TELEFONO_3 = "El teléfono no debe tener menos de 3 caracteres"
ERROR_TELEFONO_255 = "El teléfono no debe tener más de 255 caracteres"
ERROR_CCV_FORMATO = "El CCV sólo debe contener dígitos"
ERROR_CCV_3 = "El CCV no debe tener menos de 3 dígitos"
ERROR_CCV_4 = "El CCV no debe tener más de 4 dígitos"

REGEX_EMAIL = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
REGEX_URL = r"^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})$"
REGEX_NUMERO = r"[0-9]"
REGEX_NUMEROS = r"^[0-9]+$"
REGEX_MAYUSCULA = r"[A-ZÑÉÓÚÍÜ]"
REGEX_MAYUSCULAS = r"^[A-ZÑÁÉÓÚÍÜ ]+$"
REGEX_MINUSCULA = r"[a-zñéóúíü]"
REGEX_C_ESPECIAL = r"[?\-*!@#$/(){}=.,;:]"
REGEX_FECHA = r"^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$"
REGEX_TELEFONO = r"^(\(\+?\d+\)|\+?[\d A-Z]*)[\d A-Z]*(\([\d A-Z]+\))*[\d A-Z]*$"

class LogicaCaja(FachadaCajaDeSeguridad):

    def __init__(self)->None:
        super().__init__()

        Base.metadata.create_all(engine)
        self.session=Session()

        # Si no existe ninguna caja en la base de datos, crea una nueva caja
        caja = self.session.query(Caja).first()
        if caja is None:
            caja = Caja()
            caja.clave_maestra = 'clave'
            self.session.add(caja)
            self.session.commit()

        self.caja = caja

    def dar_claveMaestra(self) -> str:
        ''' Retorna la clave maestra de la caja de seguridad
        Rertorna:
            (string): La clave maestra de la caja de seguridad
        '''
        return self.caja.clave_maestra

    def mapear_elemento(self, elemento: Elemento) -> TipoElemento:
        ''' Mapea un elemento (del modelo) a un diccionario para la interfaz gráfica
        Parámetros:
            elemento (Elemento): Elemento a mapear
        Retorna:
            (dict): Diccionario con los datos para la interfaz gráfica
        '''
        if elemento.tipo == TIPO_IDENTIFICACION:
            return TipoElemento(nombre_elemento=elemento.nombre, 
                                notas=elemento.nota, 
                                tipo=elemento.tipo,
                                numero=elemento.numero,
                                nombre=elemento.nombre_completo,
                                fecha_venc=elemento.vencimiento.isoformat(),
                                fecha_nacimiento=elemento.nacimiento.isoformat(),
                                fecha_exp=elemento.expedicion.isoformat())
        if elemento.tipo == TIPO_SECRETO:
            return TipoElemento(nombre_elemento=elemento.nombre, 
                                notas=elemento.nota, 
                                tipo=elemento.tipo,
                                clave=elemento.clave.nombre, 
                                secreto=elemento.secreto,
                                ) 
        if elemento.tipo == TIPO_LOGIN:
            return TipoElemento(nombre_elemento=elemento.nombre, 
                                notas=elemento.nota, 
                                tipo=elemento.tipo,
                                clave=elemento.clave.nombre, 
                                email=elemento.email, 
                                usuario=elemento.usuario,
                                url=elemento.url, 
                                )    
        if elemento.tipo == TIPO_TARJETA:
            return TipoElemento(nombre_elemento=elemento.nombre, 
                                notas=elemento.nota, 
                                tipo=elemento.tipo,
                                clave=elemento.clave.nombre, 
                                numero=elemento.numero, 
                                titular=elemento.titular,
                                ccv=elemento.codigo_seguridad,
                                direccion=elemento.direccion,
                                telefono=elemento.telefono, 
                                fecha_venc=elemento.vencimiento.isoformat(),
                                )   
          
    def dar_elementos(self) -> List[TipoElemento]:
        ''' Retorna la lista de elementos de la caja de seguridad
        Retorna:
            (list): La lista con los dict o los objetos de los elementos
        '''
        return [self.mapear_elemento(elemento) for elemento in self.caja.elementos.order_by(Elemento.nombre)]

    def dar_elemento(self, id_elemento: int) -> TipoElemento:
        ''' Retorna un elemento de la caja de seguridad
        Parámetros:
            id_elemento (int): El identificador del elemento a retornar
        Retorna:
            (dict): El elemento identificado con id_elemento
        '''
        # Nota: id_clave no es el id de un elemento en la base de datos sino el index en la lista que retorna dar_elementos
        #       por eso aquí no es posible filtrar por id
        return self.mapear_elemento(self.caja.elementos.order_by(Elemento.nombre).offset(id_elemento).first())
    
    def eliminar_elemento(self, id):
        ''' Elimina un elemento de la lista de elementos
        Parámetros:
            id (int): El id del elemento a eliminar_clave
        '''
        # Nota: id no es el id de un elemento en la base de datos sino el index en la lista que retorna dar_elementos
        #       por eso aquí no es posible filtrar por id
        elemento = self.caja.elementos.order_by(Elemento.nombre).offset(id).first()
        self.session.delete(elemento)
        self.session.commit()

    def mapear_clave_favorita(self, clave: ClaveFavorita) -> TipoClaveFavorita:
        ''' Mapea una clave favorita (del modelo) a un diccionario para la interfaz gráfica
        Parámetros:
            clave (ClaveFavorita): Clave favorita a mapear
        Retorna:
            (dict): Diccionario con los datos para la interfaz gráfica
        '''
        return TipoClaveFavorita(nombre=clave.nombre, clave=clave.clave, pista=clave.pista)

    def dar_claves_favoritas(self) -> List[TipoClaveFavorita]:
        ''' Retorna la lita de claves favoritas
        Retorna:
            (list): La lista con los dict o los objetos de las claves favoritas
        '''
        return [self.mapear_clave_favorita(x) for x in self.caja.claves.order_by(ClaveFavorita.nombre)]

    def dar_clave_favorita(self, id_clave: int) -> TipoClaveFavorita:
        ''' Retorna una clave favoritas
        Parámetros:
            id_clave (int): El identificador de la clave favorita a retornar
        Retorna:
            (dict): La clave favorita identificada con id_clave
        '''
        # Nota: id_clave no es el id de una clave favorita en la base de datos sino el index en la lista que retorna dar_claves_favoritas
        #       por eso aquí no es posible filtrar por id
        return self.mapear_clave_favorita(self.caja.claves.order_by(ClaveFavorita.nombre).offset(id_clave).first())

    def eliminar_clave(self, id: int):
        ''' Elimina una clave favorita
        Parámetros:
            id (int): El id de la clave favorita a borrar
        '''
        # Nota: id no es el id de una clave favorita en la base de datos sino el index en la lista que retorna dar_claves_favoritas
        #       por eso aquí no es posible filtrar por id
        clave = self.caja.claves.order_by(ClaveFavorita.nombre).offset(id).first()
        self.session.delete(clave)
        self.session.commit()

    def validar_eliminar_clave(self, id):
        ''' Validar que se pueda eliminar una clave favorita
        Parámetros:
            id (int): El id de la clave favorita a borrar
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        clave = self.caja.claves.order_by(ClaveFavorita.nombre).offset(id).first()
        total_elementos = (
            self.caja.elementos.join(Login).filter(Login.clave == clave).count() +
            self.caja.elementos.join(Tarjeta).filter(Tarjeta.clave == clave).count() +
            self.caja.elementos.join(Secreto).filter(Secreto.clave == clave).count()
        )
        if total_elementos > 0:
            return ERROR_CLAVE_UTILIZADA

        return ""

    def dar_clave(self, nombre_clave: str) -> str:
        ''' Retorna la clave asignada a una clave favorita
        Parámetros:
            nombre_clave (string): El nombre de la clave favorita
        Retorna:
            (string): La clave asignada a la clave favorita del parámetro
        '''
        return self.caja.claves.filter(ClaveFavorita.nombre==nombre_clave).first().clave

    def validar_crear_editar_clave(self, id: int, nombre: str, clave: str, pista: str) -> str:
        
        ''' Valida que se pueda crear o editar una clave favorita
        Parámetros:
            id (int): El identificador de la clave a editar o -1 en case de crear una nueva clave
            nombre (string): El nombre de la clave favorita
            clave (string): El password o clae de la clave favorita
            pista (string): La pista para recordar la clave favorita
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        if len(nombre) < 1:
            return ERROR_NOMBRE_1
        if len (nombre) > 255:
            return ERROR_NOMBRE_255
        if len(clave) < 3:
            return ERROR_CLAVE_3
        if len (clave) > 255:
            return ERROR_CLAVE_255
        if len(pista) < 3:
            return ERROR_PISTA_3
        if len (pista) > 255:
            return ERROR_PISTA_255

        # Si estamos creando o si estamos editanto y el nombre de la clave ha cambiado, tenemos que comprabar que una clave con este nombre aun no existe
        comprabar_nombre = (id == -1) or (nombre != self.dar_clave_favorita(id)["nombre"])

        if comprabar_nombre and (self.caja.claves.filter(ClaveFavorita.nombre==nombre).count() > 0):
            return ERROR_ELEMENTO_EXISTENTE

        return ""

    def crear_clave(self, nombre: str, clave: str, pista: str) -> None:
        ''' Crea una clave favorita
        Parámetros:
            nombre (string): El nombre de la clave favorita
            clave (string): El password o clae de la clave favorita
            pista (string): La pista para recordar la clave favorita
        '''
        clave1 = ClaveFavorita()
        clave1.nombre = nombre
        clave1.clave = clave
        clave1.pista = pista

        self.caja.claves.append(clave1)
        self.session.commit()

    def editar_clave(self, id: int, nombre: str, clave: str, pista: str) -> None:
        ''' Edita una clave favorita
        Parámetros:
            id (int): El identificador de la clave favorita
            nombre (string): El nombre de la clave favorita
            clave (string): El password o clae de la clave favorita
            pista (string): La pista para recordar la clave favorita
        '''
        # Nota: id no es el id de una clave favorita en la base de datos sino el index en la lista que retorna dar_claves_favoritas
        #       por eso aquí no es posible filtrar por id
        c = self.caja.claves.order_by(ClaveFavorita.nombre).offset(id).first()
        c.nombre = nombre
        c.clave = clave
        c.pista = pista
        self.session.commit()

    def generar_clave(self) -> str:
        ''' Genera una clave para una clave favorita
        Retorna:
            (string): La clave generada
        '''
        GRUPO_MAYUSCULA = "ABCDEFGHIJKLMNOPQRSTUVWXYZÑÉÓÚÍÜ"
        GRUPO_MINUSCULA = "abcdefghijklmnopqrstuvwxyzñéóúíü"
        GRUPO_NUMEROS = "0123456789"
        GRUPO_ESPECIALES = "?-*!@#$/(){}=.,;:"

        # Toma entre 2 y 4 caracters de cada grupo
        clave = [random.choice(GRUPO_MAYUSCULA) for _ in range(random.randint(2, 4))]
        clave += [random.choice(GRUPO_MINUSCULA) for _ in range(random.randint(2, 4))]
        clave += [random.choice(GRUPO_NUMEROS) for _ in range(random.randint(2, 4))]
        clave += [random.choice(GRUPO_ESPECIALES) for _ in range(random.randint(2, 4))]

        random.shuffle(clave)

        return ''.join(clave)

    def validar_crear_editar_login(self, id: int, nombre: str, email: str, usuario: str, password: str, url: str, notas: str) -> str:
        ''' Valida que un login se pueda crear o editar
        Parámetros:
            id (int): El identificador del elemento a editar o -1 en case de crear un nuevo elemento
            nombre (string): El nombre del elemento
            email (string): El email del elemento
            usuario (string): El usuario del login
            password (string): El nombre de clave favorita del elemento
            url (string): El URL del login
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        if len(nombre) < 1:
            return ERROR_NOMBRE_1
        if len(nombre) > 255:
            return ERROR_NOMBRE_255
        if len(usuario) < 1:
            return ERROR_USUARIO_1
        if len(usuario) > 255:
            return ERROR_USUARIO_255
        if len(notas) < 3:
            return ERROR_NOTAS_3
        if len(notas) > 512:
            return ERROR_NOTAS_512
        if not re.match(REGEX_EMAIL, email):
            return ERROR_FORMATO_EMAIL
        if len(url) > 512:
            return ERROR_URL_512
        if not re.match(REGEX_URL, url):
            return ERROR_FORMAT_URL
        
        # Si estamos creando o si estamos editanto y el nombre de la clave ha cambiado, tenemos que comprabar que una clave con este nombre aun no existe
        comprabar_nombre = (id == -1) or (nombre != self.dar_elemento(id)["nombre_elemento"])

        if comprabar_nombre and (self.caja.elementos.filter(Elemento.nombre==nombre).count() > 0):
            return ERROR_ELEMENTO_EXISTENTE
        
        if self.caja.claves.filter(ClaveFavorita.nombre==password).count() < 1:
            return ERROR_ASIGNADO_CLAVE
        
        return ""

    def crear_login(self, nombre: str, email: str, usuario: str, password: str, url: str, notas: str) -> None:
        ''' Crea un elemento login
        Parámetros:
            nombre (string): El nombre del elemento
            email (string): El email del elemento
            usuario (string): El usuario del login
            password (string): El nombre de clave favorita del elemento
            url (string): El URL del login
            notas (string): Las notas del elemento
        '''
        l = Login()
        l.nombre = nombre
        l.email = email
        l.usuario = usuario
        l.clave = self.caja.claves.filter(ClaveFavorita.nombre==password).first()
        l.url=url
        l.nota = notas

        self.caja.elementos.append(l)
        self.session.commit()

    def editar_login(self, id: int, nombre: str, email: str, usuario: str, password: str, url: str, notas: str):
        ''' Edita un elemento login
        Parámetros:
            nombre (string): El nombre del elemento
            email (string): El email del elemento
            usuario (string): El usuario del login
            password (string): El nombre de clave favorita del elemento
            url (string): El URL del login
            notas (string): Las notas del elemento
        '''
        l = self.caja.elementos.order_by(Elemento.nombre).offset(id).first()
        l.nombre = nombre
        l.email = email
        l.usuario = usuario
        l.clave = self.caja.claves.filter(ClaveFavorita.nombre==password).first()
        l.url=url
        l.nota = notas

        self.session.commit()
    
    def dar_reporte_seguridad(self) -> TipoReporte:
        ''' Genera la información para el reporte de seguridad
        Retorna:
            (dict): Un mapa con los valores numéricos para las llaves logins, ids, tarjetas,
            secretos, inseguras, avencer, masdeuna y nivel que conforman el reporte
        '''
        hoy_mas_3_meses=datetime.today().date()+timedelta(days=3*30)
        tarjetas_avencer=self.caja.elementos.join(Tarjeta).filter(Tarjeta.vencimiento<hoy_mas_3_meses).count()
        id_avencer=self.caja.elementos.join(Identificacion).filter(Identificacion.vencimiento<hoy_mas_3_meses).count()
        numero_ids=self.caja.elementos.filter(Elemento.tipo == TIPO_IDENTIFICACION).count()
        numero_tarjetas=self.caja.elementos.filter(Elemento.tipo == TIPO_TARJETA).count()
        elementos_que_puede_vencer=numero_ids+numero_tarjetas
        elementos_avencer=tarjetas_avencer+id_avencer
        if elementos_que_puede_vencer== 0:
            v=1.0
        else:
            v=(elementos_que_puede_vencer-elementos_avencer)/(elementos_que_puede_vencer)

        repetida=0
        max_elementos=0
        seguras=0

        for x in self.caja.claves:
            total_elementos = (self.caja.elementos.join(Login).filter(Login.clave==x).count()+
                self.caja.elementos.join(Tarjeta).filter(Tarjeta.clave==x).count()+
                self.caja.elementos.join(Secreto).filter(Secreto.clave==x).count())
                        
            if total_elementos > 1:
               repetida=repetida+1

            if total_elementos>max_elementos:
                max_elementos=total_elementos
            
        if max_elementos > 3:
            r=0.0
        elif max_elementos > 1:
            r=0.5
        else:
            r=1.0

        for x in self.caja.claves:
            if len(x.clave) < 8:
                continue
            if not re.search(REGEX_NUMERO, x.clave):
                continue
            if not re.search(REGEX_MAYUSCULA, x.clave):
                continue
            if not re.search(REGEX_MINUSCULA, x.clave):
                continue
            if not re.search(REGEX_C_ESPECIAL, x.clave):
                continue
            if " " in x.clave:
                continue
            seguras=seguras+1

        total_claves=self.caja.claves.count()

        if total_claves== 0:
            sc=1.0
        else:
            sc= seguras/total_claves
        
        return TipoReporte(
            logins=self.caja.elementos.filter(Elemento.tipo == TIPO_LOGIN).count() ,
            ids=numero_ids,
            tarjetas=numero_tarjetas,
            secretos=self.caja.elementos.filter(Elemento.tipo == TIPO_SECRETO).count(),
            inseguras=total_claves-seguras,
            avencer=elementos_avencer,
            masdeuna=repetida,
            nivel=0.5*sc+0.2*v+0.3*r
        ) 
        
    def validar_crear_editar_tarjeta(self, id: int, nombre_elemento: str, numero: str, titular: str, fvencimiento: str, ccv: str, clave: str, direccion: str, telefono: str, notas: str):
        ''' Valida que una tarjeta se pueda crear o editar
        Parámetros:
            id (int): El identificador del elemento a editar o -1 en case de crear un nuevo elemento
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            titular (string): El nombre del titular de la tarjeta
            fvencimiento (string): La fecha de vencimiento en la tarjeta
            ccv (string): El código de seguridad en la tarjeta
            clave (string): El nombre de clave favorita del elemento
            direccion (string): La dirección del titular de la tarjeta
            telefono (string): El número de teléfono del titular de la tarjeta
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        if len(nombre_elemento) < 1:
            return ERROR_NOMBRE_1
        if len(nombre_elemento) > 255:
            return ERROR_NOMBRE_255
        if len(titular) < 3:
            return ERROR_TITULAR_3
        if len(titular) > 255:
            return ERROR_TITULAR_255
        if not re.match(REGEX_MAYUSCULAS, titular):
            return ERROR_TITULAR_FORMATO
        if len(notas) < 3:
            return ERROR_NOTAS_3
        if len(notas) > 512:
            return ERROR_NOTAS_512
        if not re.match(REGEX_NUMEROS, numero):
            return ERROR_NUMERO_DIGITOS
        if len(numero) < 3:
            return ERROR_NUMERO_3
        if len(numero) > 255:
            return ERROR_NUMERO_255
        if not re.match(REGEX_NUMEROS, ccv):
            return ERROR_CCV_FORMATO
        if len(ccv) < 3:
            return ERROR_CCV_3
        if len(ccv) > 4:
            return ERROR_CCV_4
        if not re.match(REGEX_FECHA, fvencimiento):
            return ERROR_FECHA_VENCIMIENTO
        if len(telefono) < 3:
            return ERROR_TELEFONO_3
        if len(telefono) > 255:
            return ERROR_TELEFONO_255
        if not re.match(REGEX_TELEFONO, telefono):
            return ERROR_TELEFONO_FORMATO
        if len(direccion) < 3:
            return ERROR_DIRECCION_3
        if len(direccion) > 255:
            return ERROR_DIRECCION_255
        if self.caja.claves.filter(ClaveFavorita.nombre==clave).count() < 1:
            return ERROR_ASIGNADO_CLAVE
        
        # Si estamos creando o si estamos editanto y el nombre de la tarjeta ha cambiado, tenemos que comprabar que un elemento con este nombre aun no existe
        comprabar_nombre = (id == -1) or (nombre_elemento != self.dar_elemento(id)["nombre_elemento"])

        if comprabar_nombre and (self.caja.elementos.filter(Elemento.nombre==nombre_elemento).count() > 0):
            return ERROR_ELEMENTO_EXISTENTE

        return ""

    def crear_tarjeta(self, nombre_elemento: str, numero: str, titular: str, fvencimiento: str, ccv: str, clave: str, direccion: str, telefono: str, notas: str):
        ''' Crea un elemento tarjeta
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            titular (string): El nombre del titular de la tarjeta
            fvencimiento (string): La feha de vencimiento en la tarjeta
            ccv (string): El código de seguridad en la tarjeta
            clave (string): El nombre de clave favorita del elemento
            direccion (string): La dirección del titular de la tarjeta
            telefono (string): El número de teléfono del titular de la tarjeta
            notas (string): Las notas del elemento
        '''
        t = Tarjeta()
        t.nombre = nombre_elemento
        t.numero = numero
        t.titular = titular
        t.vencimiento = datetime.strptime(fvencimiento, "%Y-%m-%d").date()
        t.codigo_seguridad = ccv
        t.clave = self.caja.claves.filter(ClaveFavorita.nombre==clave).first()
        t.direccion = direccion
        t.telefono = telefono
        t.nota = notas

        self.caja.elementos.append(t)
        self.session.commit()

    def editar_tarjeta(self, id: int, nombre_elemento: str, numero: str, titular: str, fvencimiento: str, ccv: str, clave: str, direccion: str, telefono: str, notas: str):
        ''' Edita un elemento tarjeta
        Parámetros:
            id (int): El identificador de la clave a editar
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            titular (string): El nombre del titular de la tarjeta
            fvencimiento (string): La feha de vencimiento en la tarjeta
            ccv (string): El código de seguridad en la tarjeta
            clave (string): El nombre de clave favorita del elemento
            direccion (string): La dirección del titular de la tarjeta
            telefono (string): El número de teléfono del titular de la tarjeta
            notas (string): Las notas del elemento
        '''
        t = self.caja.elementos.order_by(Elemento.nombre).offset(id).first()
        t.nombre = nombre_elemento
        t.numero = numero
        t.titular = titular
        t.vencimiento = datetime.strptime(fvencimiento, "%Y-%m-%d").date()
        t.codigo_seguridad = ccv
        t.clave = self.caja.claves.filter(ClaveFavorita.nombre==clave).first()
        t.direccion = direccion
        t.telefono = telefono
        t.nota = notas

        self.session.commit()

    def validar_crear_editar_id(self, id: int, nombre_elemento: str, numero: str, nombre_completo: str, fnacimiento: str, fexpedicion: str, fvencimiento: str, notas: str):
        ''' Valida que una identificación se pueda crear o editar
        Parámetros:
            id (int): El identificador del elemento a editar o -1 en case de crear un nuevo elemento
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            nombre_completo (string): El nombre completo de la persona en la identificación
            fnacimiento (string): La fecha de nacimiento de la persona en la identificación
            fexpedicion (string): La fecha de expedición en la identificación
            fvencimiento (string): La feha de vencimiento en la identificación
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        if len(nombre_elemento) < 1:
            return ERROR_NOMBRE_1
        if len(nombre_elemento) > 255:
            return ERROR_NOMBRE_255
        if len(notas) < 3:
            return ERROR_NOTAS_3
        if len(notas) > 512:
            return ERROR_NOTAS_512
        if len(nombre_completo) < 3:
            return ERROR_NOMBRE_COMPLETO_3
        if len(nombre_completo) > 255:
            return ERROR_NOMBRE_COMPLETO_255
        if not re.match(REGEX_NUMEROS, numero):
            return ERROR_NUMERO_DIGITOS
        if len(numero) < 3:
            return ERROR_NUMERO_3
        if len(numero) > 20:
            return ERROR_NUMERO_20
        if not re.match(REGEX_FECHA, fvencimiento):
            return ERROR_FECHA_VENCIMIENTO
        if not re.match(REGEX_FECHA, fexpedicion):
            return ERROR_FECHA_EXPEDICION
        if not re.match(REGEX_FECHA, fnacimiento):
            return ERROR_FECHA_NACIMIENTO
        
        # Si estamos creando o si estamos editanto y el nombre de la clave ha cambiado, tenemos que comprabar que una clave con este nombre aun no existe
        comprabar_nombre = (id == -1) or (nombre_elemento != self.dar_elemento(id)["nombre_elemento"])

        if comprabar_nombre and (self.caja.elementos.filter(Elemento.nombre==nombre_elemento).count() > 0):
            return ERROR_ELEMENTO_EXISTENTE
        return ""

    def crear_id(self, nombre_elemento: str , numero: str, nombre_completo: str, fnacimiento: str, fexpedicion: str, fvencimiento: str, notas: str):
        ''' Crea un elemento identificación
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            nombre_completo (string): El nombre completo de la persona en la identificación
            fnacimiento (string): La fecha de nacimiento de la persona en la identificación
            fexpedicion (string): La fecha de expedición en la identificación
            fvencimiento (string): La feha de vencimiento en la identificación
            notas (string): Las notas del elemento
        '''
        i = Identificacion()
        i.nombre = nombre_elemento
        i.nota = notas
        i.numero = numero
        i.nombre_completo = nombre_completo
        i.nacimiento = datetime.strptime(fnacimiento, "%Y-%m-%d").date()
        i.expedicion = datetime.strptime(fexpedicion, "%Y-%m-%d").date()
        i.vencimiento = datetime.strptime(fvencimiento, "%Y-%m-%d").date()
        self.caja.elementos.append(i)
        self.session.commit()

    def editar_id(self, id: int, nombre_elemento: str, numero: str, nombre_completo: str, fnacimiento: str, fexpedicion: str, fvencimiento: str, notas: str):
        ''' Edita un elemento identificación
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            nombre_completo (string): El nombre completo de la persona en la identificación
            fnacimiento (string): La fecha de nacimiento de la persona en la identificación
            fexpedicion (string): La fecha de expedición en la identificación
            fvencimiento (string): La feha de vencimiento en la identificación
            notas (string): Las notas del elemento
        '''
        i = self.caja.elementos.order_by(Elemento.nombre).offset(id).first()
        i.nombre = nombre_elemento
        i.nota = notas
        i.numero = numero
        i.nombre_completo = nombre_completo
        i.nacimiento = datetime.strptime(fnacimiento, "%Y-%m-%d").date()
        i.expedicion = datetime.strptime(fexpedicion, "%Y-%m-%d").date()
        i.vencimiento = datetime.strptime(fvencimiento, "%Y-%m-%d").date()
        
        self.session.commit()

    def validar_crear_editar_secreto(self, id: int, nombre: str, secreto: str, clave: str, notas: str):
        ''' Valida que se pueda crear o editar un elemento secreto
        Parámetros:
            id (int): El identificador del elemento a editar o -1 en case de crear un nuevo elemento
            nombre (string): El nombre del elemento
            secreto (string): El secreto del elemento
            clave (string): El nombre de clave favorita del elemento
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        if len(nombre) < 1:
            return ERROR_NOMBRE_1
        if len(nombre) > 255:
            return ERROR_NOMBRE_255
        if len(notas) < 3:
            return ERROR_NOTAS_3
        if len(notas) > 512:
            return ERROR_NOTAS_512
        if len(secreto) < 3:
            return ERROR_SECRETO_3
        if len(secreto) > 255:
            return ERROR_SECRETO_255
        if self.caja.claves.filter(ClaveFavorita.nombre==clave).count() < 1:
            return ERROR_ASIGNADO_CLAVE

        # Si estamos creando o si estamos editanto y el nombre de la clave ha cambiado, tenemos que comprabar que una clave con este nombre aun no existe
        comprabar_nombre = (id == -1) or (nombre != self.dar_elemento(id)["nombre_elemento"])

        if comprabar_nombre and (self.caja.elementos.filter(Elemento.nombre==nombre).count() > 0):
            return ERROR_ELEMENTO_EXISTENTE
        return ""

    def crear_secreto(self, nombre: str, secreto: str, clave: str, notas: str):
        ''' Crea un elemento secreto
        Parámetros:
            nombre (string): El nombre del elemento
            secreto (string): El secreto del elemento
            clave (string): El nombre de clave favorita del elemento
            notas (string): Las notas del elemento
        '''
        s = Secreto()
        s.nombre = nombre
        s.nota = notas
        s.secreto = secreto
        s.clave = self.caja.claves.filter(ClaveFavorita.nombre==clave).first()
        self.caja.elementos.append(s)
        self.session.commit()

    def editar_secreto(self, id: int, nombre: str, secreto: str, clave: str, notas: str):
        ''' Edita un elemento secreto
        Parámetros:
            id (int): El identificador del elemento a editar
            nombre (string): El nombre del elemento
            secreto (string): El secreto del elemento
            clave (string): El nombre de clave favorita del elemento
            notas (string): Las notas del elemento
        '''
        s = self.caja.elementos.order_by(Elemento.nombre).offset(id).first()
        s.nombre = nombre
        s.nota = notas
        s.secreto = secreto
        s.clave = self.caja.claves.filter(ClaveFavorita.nombre==clave).first()
        self.session.commit()
