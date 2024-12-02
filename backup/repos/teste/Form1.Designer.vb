<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        Button1 = New Button()
        TextBox2 = New TextBox()
        Label1 = New Label()
        Button2 = New Button()
        Button3 = New Button()
        Button4 = New Button()
        Label3 = New Label()
        SuspendLayout()
        ' 
        ' Button1
        ' 
        Button1.Location = New Point(37, 311)
        Button1.Name = "Button1"
        Button1.Size = New Size(75, 23)
        Button1.TabIndex = 0
        Button1.Text = "Adicionar"
        Button1.UseVisualStyleBackColor = True
        Button1.Visible = False
        ' 
        ' TextBox2
        ' 
        TextBox2.Location = New Point(12, 90)
        TextBox2.Name = "TextBox2"
        TextBox2.Size = New Size(233, 23)
        TextBox2.TabIndex = 2
        ' 
        ' Label1
        ' 
        Label1.AutoSize = True
        Label1.Font = New Font("Showcard Gothic", 15F, FontStyle.Regular, GraphicsUnit.Point)
        Label1.Location = New Point(236, 0)
        Label1.Name = "Label1"
        Label1.Size = New Size(237, 26)
        Label1.TabIndex = 3
        Label1.Text = "Cadastro de clientes"
        ' 
        ' Button2
        ' 
        Button2.Location = New Point(37, 340)
        Button2.Name = "Button2"
        Button2.Size = New Size(75, 23)
        Button2.TabIndex = 4
        Button2.Text = "Remover"
        Button2.UseVisualStyleBackColor = True
        Button2.Visible = False
        ' 
        ' Button3
        ' 
        Button3.Location = New Point(251, 90)
        Button3.Name = "Button3"
        Button3.Size = New Size(75, 23)
        Button3.TabIndex = 5
        Button3.Text = "Validar"
        Button3.UseVisualStyleBackColor = True
        ' 
        ' Button4
        ' 
        Button4.Location = New Point(37, 369)
        Button4.Name = "Button4"
        Button4.Size = New Size(75, 23)
        Button4.TabIndex = 6
        Button4.Text = "Conferir"
        Button4.UseVisualStyleBackColor = True
        Button4.Visible = False
        ' 
        ' Label3
        ' 
        Label3.AutoSize = True
        Label3.Location = New Point(12, 74)
        Label3.Name = "Label3"
        Label3.Size = New Size(26, 15)
        Label3.TabIndex = 8
        Label3.Text = "Cpf"
        ' 
        ' Form1
        ' 
        AutoScaleDimensions = New SizeF(7F, 15F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(800, 450)
        Controls.Add(Label3)
        Controls.Add(Button4)
        Controls.Add(Button3)
        Controls.Add(Button2)
        Controls.Add(Label1)
        Controls.Add(TextBox2)
        Controls.Add(Button1)
        Name = "Form1"
        Text = "Form1"
        ResumeLayout(False)
        PerformLayout()
    End Sub

    Friend WithEvents Button1 As Button
    Friend WithEvents TextBox2 As TextBox
    Friend WithEvents Label1 As Label
    Friend WithEvents Button2 As Button
    Friend WithEvents Button3 As Button
    Friend WithEvents Button4 As Button
    Friend WithEvents Label3 As Label
End Class
