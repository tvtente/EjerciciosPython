class AmountError(ValueError):
    # Error de validación para importes inválidos introducidos por el usuario.
    def __init__(self, message: str, *, code: str = "invalid", raw_input: str | None = None):
        super().__init__(message)
        self.code = code  # Código interno del tipo de error.
        self.raw_input = raw_input  # Valor original introducido, para depuración.

    def __str__(self):
        return self.args[0]
