class Cuenta:
    # Representa una cuenta bancaria con titular y saldo.
    def __init__(self, titular, saldo=0):
        self._titular = titular
        self._saldo = saldo  # Saldo almacenado en céntimos (int).

    def __str__(self):
        return f'Titular: {self._titular} | Saldo actual: {self._saldo}'

    @property
    def get_titular(self):
        return self._titular

    @property
    def get_saldo(self):
        return self._saldo

    def depositar(self, valor):
        # Suma el importe al saldo y lo devuelve.
        self._saldo += valor
        return valor

    def retirar(self, valor):
        # Si no hay fondos suficientes, no se realiza el retiro.
        if valor > self._saldo:
            return None

        self._saldo -= valor
        return valor
