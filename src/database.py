from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.models import Base
import os

# Caminho do banco configurável por variável de ambiente (SQLite padrão ou PostgreSQL)
DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'project.db'))
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
    sqlite_file = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(sqlite_file)), exist_ok=True)

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

# Session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Criar tabelas caso ainda não existam
Base.metadata.create_all(bind=engine)

# Garantir coluna subjects no SQLite se o banco já existia e sanitizar integridade de disciplinas (1 a 6 por docente)
with engine.connect() as conn:
    from sqlalchemy import text
    import json
    try:
        conn.execute(text("SELECT subjects FROM Teacher LIMIT 1"))
    except Exception:
        conn.execute(text("ALTER TABLE Teacher ADD COLUMN subjects JSON DEFAULT '[]'"))
        conn.commit()

    try:
        result = conn.execute(text("SELECT id, subjects FROM Teacher")).fetchall()
        for row in result:
            t_id, raw_sub = row[0], row[1]
            sub_list = []
            if raw_sub:
                if isinstance(raw_sub, str):
                    try:
                        sub_list = json.loads(raw_sub)
                    except Exception:
                        sub_list = []
                elif isinstance(raw_sub, list):
                    sub_list = raw_sub

            if not isinstance(sub_list, list) or len(sub_list) == 0:
                sub_list = ["Geral"]
            elif len(sub_list) > 6:
                sub_list = sub_list[:6]

            json_str = json.dumps(sub_list)
            conn.execute(text("UPDATE Teacher SET subjects = :sub WHERE id = :id"), {"sub": json_str, "id": t_id})
        conn.commit()
    except Exception:
        pass

    try:
        conn.execute(text("SELECT subject FROM Allocation LIMIT 1"))
    except Exception:
        conn.execute(text("ALTER TABLE Allocation ADD COLUMN subject VARCHAR"))
        conn.commit()

    try:
        conn.execute(text("SELECT must_change_password FROM User LIMIT 1"))
    except Exception:
        conn.execute(text("ALTER TABLE User ADD COLUMN must_change_password BOOLEAN DEFAULT 0"))
        conn.commit()


def seed_subslots():
    from src.models import SubslotTimeInterval
    db = SessionLocal()
    try:
        existing_codes = set(r[0] for r in db.query(SubslotTimeInterval.code).all())
        default_subslots = [
            # Matutino
            SubslotTimeInterval(id="subslot-m1", code="M1", shift="matutino", class_number=1, start_time="07:00", end_time="07:50", is_interval=False),
            SubslotTimeInterval(id="subslot-m2", code="M2", shift="matutino", class_number=2, start_time="07:50", end_time="08:40", is_interval=False),
            SubslotTimeInterval(id="subslot-m3", code="M3", shift="matutino", class_number=3, start_time="08:40", end_time="09:30", is_interval=False),
            SubslotTimeInterval(id="subslot-m-int", code="M_INT", shift="matutino", class_number=None, start_time="09:30", end_time="09:45", is_interval=True),
            SubslotTimeInterval(id="subslot-m4", code="M4", shift="matutino", class_number=4, start_time="09:45", end_time="10:35", is_interval=False),
            SubslotTimeInterval(id="subslot-m5", code="M5", shift="matutino", class_number=5, start_time="10:35", end_time="11:25", is_interval=False),
            SubslotTimeInterval(id="subslot-m6", code="M6", shift="matutino", class_number=6, start_time="11:25", end_time="12:15", is_interval=False),

            # Vespertino
            SubslotTimeInterval(id="subslot-t1", code="T1", shift="vespertino", class_number=1, start_time="13:00", end_time="13:50", is_interval=False),
            SubslotTimeInterval(id="subslot-t2", code="T2", shift="vespertino", class_number=2, start_time="13:50", end_time="14:40", is_interval=False),
            SubslotTimeInterval(id="subslot-t3", code="T3", shift="vespertino", class_number=3, start_time="14:40", end_time="15:30", is_interval=False),
            SubslotTimeInterval(id="subslot-t-int", code="T_INT", shift="vespertino", class_number=None, start_time="15:30", end_time="15:45", is_interval=True),
            SubslotTimeInterval(id="subslot-t4", code="T4", shift="vespertino", class_number=4, start_time="15:45", end_time="16:35", is_interval=False),
            SubslotTimeInterval(id="subslot-t5", code="T5", shift="vespertino", class_number=5, start_time="16:35", end_time="17:25", is_interval=False),
            SubslotTimeInterval(id="subslot-t6", code="T6", shift="vespertino", class_number=6, start_time="17:25", end_time="18:15", is_interval=False),

            # Noturno
            SubslotTimeInterval(id="subslot-n1", code="N1", shift="noturno", class_number=1, start_time="19:00", end_time="19:50", is_interval=False),
            SubslotTimeInterval(id="subslot-n2", code="N2", shift="noturno", class_number=2, start_time="19:50", end_time="20:40", is_interval=False),
            SubslotTimeInterval(id="subslot-n3", code="N3", shift="noturno", class_number=3, start_time="20:40", end_time="21:30", is_interval=False),
            SubslotTimeInterval(id="subslot-n-int", code="N_INT", shift="noturno", class_number=None, start_time="21:30", end_time="21:45", is_interval=True),
            SubslotTimeInterval(id="subslot-n4", code="N4", shift="noturno", class_number=4, start_time="21:45", end_time="22:35", is_interval=False),
            SubslotTimeInterval(id="subslot-n5", code="N5", shift="noturno", class_number=5, start_time="22:35", end_time="23:25", is_interval=False),
            SubslotTimeInterval(id="subslot-n6", code="N6", shift="noturno", class_number=6, start_time="23:25", end_time="00:15", is_interval=False),
        ]
        to_add = [s for s in default_subslots if s.code not in existing_codes]
        if to_add:
            db.bulk_save_objects(to_add)
            db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def seed_users():
    from src.models import User
    from src.api.auth import hash_password
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.email == "admin@classsync.ai").first()
        if not admin_user:
            admin_user = User(
                id="u-admin-001",
                name="Gestor Principal",
                email="admin@classsync.ai",
                password_hash=hash_password("admin123"),
                role="gestor",
                department="Administração Geral",
                is_active=True,
                must_change_password=False
            )
            db.add(admin_user)
            db.commit()

        doctor_user = db.query(User).filter(User.email == "doctor@classsync.ai").first()
        if not doctor_user:
            doctor_user = User(
                id="u-doctor-001",
                name="Super Administrador Geral",
                email="doctor@classsync.ai",
                password_hash=hash_password("Doctor@2026"),
                role="doctor-chef",
                department="Plataforma Global",
                is_active=True,
                must_change_password=False
            )
            db.add(doctor_user)
            db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

seed_subslots()
seed_users()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


