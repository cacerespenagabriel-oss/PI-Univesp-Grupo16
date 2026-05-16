from database import engine
import models

print("🔄 Conectando ao Neon e criando tabelas...")
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso no Neon!")
except Exception as e:
    print(f"❌ Erro ao criar tabelas: {e}")