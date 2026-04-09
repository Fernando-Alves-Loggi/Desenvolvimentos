import base64

def gerar_auth_basic(usuario, senha):
    # Formata a string como 'usuario:senha'
    credenciais = f"{usuario}:{senha}"
    
    # Converte para bytes e depois para base64
    credenciais_bytes = credenciais.encode('ascii')
    base64_bytes = base64.b64encode(credenciais_bytes)
    
    # Transforma de volta para string
    base64_string = base64_bytes.decode('ascii')
    
    return f"Basic {base64_string}"

# Exemplo de uso baseado na documentação
meu_usuario = "admin"
minha_senha = "D3A8475D2B0A5BE8017DBF9F6C812707" # Exemplo do documento 

header_auth = gerar_auth_basic(meu_usuario, minha_senha)
print(f"Authorization: {header_auth}")