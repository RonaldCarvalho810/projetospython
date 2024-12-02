Imports System.Buffers

Public Class Form1
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load

    End Sub

    Private Sub Label1_Click(sender As Object, e As EventArgs) Handles Label1.Click

    End Sub
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        Dim i As Integer
        Dim soma As Long
        Dim resto As Integer
        Dim digito1 As Integer
        Dim digito2 As Integer
        Dim pesos1(8) As Integer
        Dim pesos2(9) As Integer
        Dim cpf As String

        ' Captura e limpa o CPF (removendo pontos e traços)
        cpf = Replace(TextBox2.Text, ".", "")
        cpf = Replace(cpf, "-", "")
        cpf = Trim(cpf)

        ' Verifica se o CPF tem 11 dígitos
        If Len(cpf) <> 11 Then
            MsgBox("O CPF precisa ter 11 dígitos.", vbExclamation, "Erro")
            Exit Sub
        End If

        ' Verifica se todos os dígitos são iguais (exemplo: 11111111111)
        If cpf = New String(cpf(0), 11) Then
            MsgBox("CPF inválido! Todos os dígitos são iguais.", vbExclamation, "Erro")
            Exit Sub
        End If

        ' Define os pesos para o cálculo dos dígitos verificadores
        For i = 0 To 8
            pesos1(i) = 10 - i
        Next
        For i = 0 To 9
            pesos2(i) = 11 - i
        Next

        ' Cálculo do primeiro dígito verificador
        soma = 0
        For i = 1 To 9
            soma = soma + CInt(Mid(cpf, i, 1)) * pesos1(i - 1)
        Next
        resto = soma Mod 11
        If resto < 2 Then
            digito1 = 0
        Else
            digito1 = 11 - resto
        End If

        ' Cálculo do segundo dígito verificador
        soma = 0
        For i = 1 To 10
            If i = 10 Then
                soma = soma + digito1 * pesos2(i - 1)
            Else
                soma = soma + CInt(Mid(cpf, i, 1)) * pesos2(i - 1)
            End If
        Next
        resto = soma Mod 11
        If resto < 2 Then
            digito2 = 0
        Else
            digito2 = 11 - resto
        End If

        ' Verifica os dígitos verificadores
        If Mid(cpf, 10, 1) = CStr(digito1) And Mid(cpf, 11, 1) = CStr(digito2) Then
            MsgBox("CPF válido!", vbInformation, "Resultado")
        Else
            MsgBox("CPF inválido!", vbExclamation, "Resultado")
        End If
    End Sub




    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        If TextBox2.Text = "renato" Then
            MsgBox("brabo")
        Else
            MsgBox("mansinho")
        End If
    End Sub

End Class
