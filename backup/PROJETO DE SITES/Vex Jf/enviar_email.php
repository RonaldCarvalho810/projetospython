<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Coleta os dados do formulário
    $nome = $_POST['nome'];
    $data = $_POST['data'];
    $destino = $_POST['destino'];
    $contato = $_POST['contato'];
    $mensagem = $_POST['mensagem'];

    // Configurações do e-mail
    $to = "contato@vexjf.com.br"; // Substitua pelo seu endereço de e-mail
    $subject = "Nova Reserva de Viagem";
    $message = "Você recebeu uma nova reserva:\n\n" .
               "Nome: $nome\n" .
               "Data da Viagem: $data\n" .
               "Destino: $destino\n" .
               "E-mail: $contato\n" .
               "Mensagem: $mensagem\n";
    
    $headers = "From: $contato" . "\r\n" . // Define o remetente
               "Reply-To: $contato" . "\r\n"; // Resposta

    // Envia o e-mail
    if (mail($to, $subject, $message, $headers)) {
        echo "Reserva enviada com sucesso!";
    } else {
        echo "Erro ao enviar a reserva.";
    }
} else {
    echo "Método de requisição inválido.";
}
?>
