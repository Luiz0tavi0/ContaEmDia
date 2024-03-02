import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError


class TestDatabaseConnection:
    @pytest.mark.asyncio
    async def test_database_connection(self, engine: AsyncSession):
        try:
            async with engine.connect():
                assert True  # Se a conexão for bem-sucedida, o banco de dados está online
        except OperationalError:
            # Se ocorrer um erro operacional durante a tentativa de conexão, o teste falhará
            assert False, "Erro operacional ao conectar ao banco de dados"
        except Exception as e:
            # Se ocorrer qualquer outra exceção durante a tentativa de conexão, o teste falhará
            assert False, f"Erro ao conectar ao banco de dados: {e}"

