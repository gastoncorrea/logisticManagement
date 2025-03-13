
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