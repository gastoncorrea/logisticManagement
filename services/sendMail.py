
from flask_mail import Mail, Message

mail = Mail()


def send_mails(pedido):
    
    with mail.connect() as conn:
            msg = Message(
                subject="Confirmación de Pedido",
                recipients=[pedido.cliente.email],
                body=f"""
                Hola {pedido.cliente.nombre},

                Tu pedido número {pedido.nro_pedido} ha sido registrado correctamente. 
                Pronto será enviado a la dirección proporcionada.

                ¡Gracias por tu compra!

                Saludos,
                Logistica ALE GARCIA
                """
            )
            conn.send(msg)
            print(f"Correo enviado a: {pedido.cliente.email}")

    return "Correos enviados"

def send_mail_shipping(pedido):
    
    with mail.connect() as conn:
            msg = Message(
                subject="Se entregara hoy su Pedido",
                recipients=["sgarcia90.912@gmail.com"],
                body=f"""
                Hola {pedido.cliente.nombre},

                Tu pedido número {pedido.nro_pedido} será entregado hoy por uno de nuestros riders
                a la dirección proporcionada.

                ¡Gracias por tu compra!

                Saludos,
                SkyFlex Logistica
                """
            )
            conn.send(msg)
            print(f"Correo enviado a: {pedido.cliente.email}")

    return f"Correos enviados a: {pedido.cliente.email}"

def send_mail_delivered(pedido, receive):
    
    with mail.connect() as conn:
            msg = Message(
                subject="Su pedido ya fue entregado",
                recipients=["sgarcia90.912@gmail.com"],
                body=f"""
                Hola {pedido.cliente.nombre},

                Tu pedido número {pedido.nro_pedido} fue entregado en la direccion proporcionada
                y fue recibido por {receive.entrega_nombre}, Dni: {receive.entrega_dni}.

                ¡Gracias por tu compra!

                Saludos,
                SkyFlex Logistica
                """
            )
            conn.send(msg)
            print(f"Correo enviado a: {pedido.cliente.email}")

    return f"Correos enviados a: {pedido.cliente.email}"