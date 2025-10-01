from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request as StarletteRequest
from authlib.integrations.starlette_client import OAuth
import psycopg2
import os
import csv
from io import StringIO, BytesIO
from datetime import datetime, timedelta, date
from typing import Optional, Tuple, List
from pathlib import Path



# Optional imports for export formats
try:
    from openpyxl import Workbook
except Exception:
    Workbook = None  # type: ignore

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
except Exception:
    SimpleDocTemplate = None  # type: ignore

app = FastAPI()

# ==== Mount Static Files ====
if Path("public").exists():
    app.mount("/static", StaticFiles(directory="public"), name="static")

# ==== Session Middleware ====
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "super-secret-key"))

# ==== CORS ====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Konfigurasi Database ====
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "welcome-to-nuanu-new"),
    "user": os.getenv("DB_USER", "doadmin"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "welcome-to-nuanu-new-do-user-17765453-0.g.db.ondigitalocean.com"),
    "port": int(os.getenv("DB_PORT", "25060")),
    "sslmode": "require"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "Bali0361")

# ==== URL Aplikasi ====
BASE_URL = os.getenv("BASE_URL", "http://167.71.206.110")

# ==== Mikrotik Hotspot ====
GATEWAY_IP = os.getenv("GATEWAY_IP", "172.19.20.1")
HOTSPOT_USER = os.getenv("HOTSPOT_USER", "user")
HOTSPOT_PASS = os.getenv("HOTSPOT_PASS", "user")
DST_URL = os.getenv("DST_URL", "https://nuanu.com/")

# ==== Google OAuth ====
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# ==== DB Init ====
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wifi_users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            questions TEXT,
            role VARCHAR(100),
            ip_address VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

# ==== Serve Login Page ====
@app.get("/", response_class=HTMLResponse)
async def serve_login():
    login_file = Path("public/login.html")
    if login_file.exists():
        return FileResponse(login_file)
    return HTMLResponse("<h1>Login page not found</h1>", status_code=404)

# ==== Serve Admin Dashboard ====
@app.get("/admin", response_class=HTMLResponse)
async def serve_admin():
    admin_file = Path("public/admin.html")
    if admin_file.exists():
        return FileResponse(admin_file)
    return HTMLResponse("<h1>Admin page not found</h1>", status_code=404)

# ==== Save User Data (Email, Questions, Role) ====
@app.post("/api/save-user")
async def save_user(request: Request):
    data = await request.json()
    email = data.get("email")
    questions = data.get("questions", "")
    role = data.get("role", "")
    
    if not email:
        return JSONResponse({"success": False, "message": "Invalid email"}, status_code=400)

    # Get IP address
    ip_address = request.client.host if request.client else None

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO wifi_users (email, questions, role, ip_address)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (email, questions, role, ip_address))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return JSONResponse({
            "success": True,
            "message": "User data saved successfully",
            "data": {"id": user_id, "email": email}
        })
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

# ==== Get All Users (for admin) ====
@app.get("/api/users")
async def get_users(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, email, questions, role, ip_address, created_at
        FROM wifi_users
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "email": row[1],
            "questions": row[2],
            "role": row[3],
            "ip_address": row[4],
            "created_at": row[5].isoformat() if row[5] else None
        })
    
    return JSONResponse({
        "success": True,
        "count": len(users),
        "data": users
    })

# ==== Get Statistics ====
@app.get("/api/stats")
async def get_stats(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    
    # Total users
    cur.execute("SELECT COUNT(*) FROM wifi_users")
    total = cur.fetchone()[0]
    
    # Last 24 hours
    cur.execute("SELECT COUNT(*) FROM wifi_users WHERE created_at > NOW() - INTERVAL '24 hours'")
    last24h = cur.fetchone()[0]
    
    # By role
    cur.execute("""
        SELECT role, COUNT(*) as count
        FROM wifi_users
        WHERE role IS NOT NULL AND role != ''
        GROUP BY role
        ORDER BY count DESC
    """)
    role_rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    by_role = [{"role": r[0], "count": r[1]} for r in role_rows]
    
    return JSONResponse({
        "success": True,
        "stats": {
            "total": total,
            "last24hours": last24h,
            "byRole": by_role
        }
    })

# ==== Delete User ====
@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, request: Request):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM wifi_users WHERE id = %s RETURNING id", (user_id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted:
            return JSONResponse({"success": True, "message": "User deleted successfully"})
        else:
            return JSONResponse({"success": False, "message": "User not found"}, status_code=404)
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

# ==== Google Login ====
@app.get("/auth/google/login")
async def login_google(request: StarletteRequest):
    redirect_uri = f"{BASE_URL.rstrip('/')}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def auth_google_callback(request: StarletteRequest):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info:
        return JSONResponse({"status": "error", "message": "Google login failed"})

    email = user_info["email"]

    # Save or update in DB as verified
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trial_emails (email, is_verified)
        VALUES (%s, TRUE)
        ON CONFLICT (email) DO UPDATE SET is_verified = TRUE
    """, (email,))
    conn.commit()
    cur.close()
    conn.close()

    login_url = (
        f"http://{GATEWAY_IP}/login?"
        f"username={HOTSPOT_USER}&password={HOTSPOT_PASS}&dst={DST_URL}"
    )
    return RedirectResponse(url=login_url)

# ==== Dashboard Login Page ====
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_login(request: Request):
    if request.session.get("logged_in"):
        # Get page parameter from query string, default to 1
        try:
            page = int(request.query_params.get("page", 1))
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1
        # Pass-through filter params
        return await show_dashboard(
            page=page,
            date_filter=request.query_params.get("date_filter"),
            start_date_str=request.query_params.get("start_date"),
            end_date_str=request.query_params.get("end_date"),
        )

    html = """
    <html>
      <head>
        <title>Dashboard Login</title>
        <style>
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;
          }
          .login-box {
            background: white; padding: 40px; border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2); text-align: center; width: 300px;
          }
          input[type=password] { width: 100%; padding: 12px 10px; margin: 15px 0; border-radius: 6px; border: 1px solid #ccc; font-size: 16px; }
          button { background: #667eea; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; }
          button:hover { background: #5a67d8; }
        </style>
      </head>
      <body>
        <div class="login-box">
          <h2>🔒 Dashboard Login</h2>
          <form method="post" action="/dashboard">
            <input type="password" name="password" placeholder="Enter password" required>
            <button type="submit">Login</button>
          </form>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

# ==== Handle Dashboard Login ====
# ==== Handle Dashboard Login ====
@app.post("/dashboard", response_class=HTMLResponse)
async def dashboard_post(request: Request, password: str = Form(...)):
    if password != DASHBOARD_PASSWORD:
        return HTMLResponse(content="<h2>❌ Invalid password</h2><a href='/phicampdashboard'>Try again</a>", status_code=401)

    request.session["logged_in"] = True
    # Get page parameter from query string, default to 1
    try:
        page = int(request.query_params.get("page", 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1
    return await show_dashboard(page=page)

# ==== Show Dashboard ====
def _compute_date_range(
    date_filter: Optional[str], start_date_str: Optional[str], end_date_str: Optional[str]
) -> Tuple[Optional[datetime], Optional[datetime], str]:
    """Compute start and end datetime based on filter preset or custom fields.
    Returns (start_dt, end_dt, human_label).
    """
    today = date.today()

    def start_of_month(d: date) -> date:
        return d.replace(day=1)

    def end_of_month(d: date) -> date:
        next_month = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        return next_month - timedelta(days=1)

    if date_filter == "today":
        start_dt = datetime.combine(today, datetime.min.time())
        end_dt = datetime.combine(today, datetime.max.time())
        return start_dt, end_dt, "Today"
    if date_filter == "yesterday":
        y = today - timedelta(days=1)
        start_dt = datetime.combine(y, datetime.min.time())
        end_dt = datetime.combine(y, datetime.max.time())
        return start_dt, end_dt, "Yesterday"
    if date_filter == "last7":
        start_dt = datetime.combine(today - timedelta(days=6), datetime.min.time())
        end_dt = datetime.combine(today, datetime.max.time())
        return start_dt, end_dt, "Last 7 days"
    if date_filter == "last30":
        start_dt = datetime.combine(today - timedelta(days=29), datetime.min.time())
        end_dt = datetime.combine(today, datetime.max.time())
        return start_dt, end_dt, "Last 30 days"
    if date_filter == "thisMonth":
        s = start_of_month(today)
        e = end_of_month(today)
        return datetime.combine(s, datetime.min.time()), datetime.combine(e, datetime.max.time()), "This month"
    if date_filter == "prevMonth":
        first_this = start_of_month(today)
        prev_end = first_this - timedelta(days=1)
        prev_start = start_of_month(prev_end)
        return (
            datetime.combine(prev_start, datetime.min.time()),
            datetime.combine(prev_end, datetime.max.time()),
            "Previous month",
        )

    # custom or none
    if start_date_str and end_date_str:
        try:
            s_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            e_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            start_dt = datetime.combine(s_date, datetime.min.time())
            end_dt = datetime.combine(e_date, datetime.max.time())
            return start_dt, end_dt, f"{s_date.isoformat()} → {e_date.isoformat()}"
        except Exception:
            pass

    return None, None, "All time"

async def show_dashboard(page: int = 1, page_size: int = 20, date_filter: Optional[str] = None, start_date_str: Optional[str] = None, end_date_str: Optional[str] = None):
    conn = get_connection()
    cur = conn.cursor()
    
    # Build WHERE clause from date filter
    start_dt, end_dt, range_label = _compute_date_range(date_filter, start_date_str, end_date_str)
    where_sql = ""
    params: List = []
    if start_dt and end_dt:
        where_sql = "WHERE created_at BETWEEN %s AND %s"
        params.extend([start_dt, end_dt])

    # Get total count for pagination
    cur.execute(f"SELECT COUNT(*) FROM trial_emails {where_sql}", params)
    total_count = cur.fetchone()[0]
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get paginated results
    cur.execute(
        f"""
        SELECT email, created_at 
        FROM trial_emails 
        {where_sql}
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s
    """,
        (*params, page_size, offset),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Calculate pagination info
    total_pages = (total_count + page_size - 1) // page_size
    has_prev = page > 1
    has_next = page < total_pages

    # Build filter query string for pagination links
    filter_qs = ""
    if date_filter:
        filter_qs += f"&date_filter={date_filter}"
    if start_date_str:
        filter_qs += f"&start_date={start_date_str}"
    if end_date_str:
        filter_qs += f"&end_date={end_date_str}"

    html = f"""
    <html>
      <head>
        <title>Email Dashboard</title>
        <style>
          body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f3f4f6; padding: 20px; }}
          h1 {{ text-align: center; color: #333; }}
          .filters {{ background: white; border-radius: 8px; padding: 16px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }}
          .filters form {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: end; }}
          .filters label {{ font-size: 13px; color: #555; }}
          .filters select, .filters input[type=date] {{ padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px; }}
          .filters button {{ background: #4f46e5; color: white; border: none; padding: 10px 14px; border-radius: 6px; cursor: pointer; }}
          .pagination-info {{ text-align: center; margin: 10px 0; color: #666; font-size: 14px; }}
          table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
          th, td {{ padding: 12px 15px; text-align: left; }}
          th {{ background: #667eea; color: white; }}
          tr:nth-child(even) {{ background: #f2f2f2; }}
          .logout, .download {{ display: inline-block; margin: 10px; text-decoration: none; font-weight: bold; padding: 10px 15px; border-radius: 6px; }}
          .logout {{ color: #667eea; border: 1px solid #667eea; }}
          .logout:hover {{ background: #667eea; color: white; }}
          .download {{ background: #10b981; color: white; }}
          .download:hover {{ background: #059669; }}
          .buttons {{ text-align:center; margin-top: 20px; }}
          .pagination {{ text-align: center; margin: 20px 0; }}
          .pagination a {{ display: inline-block; padding: 8px 12px; margin: 0 4px; text-decoration: none; border: 1px solid #667eea; border-radius: 4px; color: #667eea; }}
          .pagination a:hover {{ background: #667eea; color: white; }}
          .pagination .current {{ background: #667eea; color: white; }}
          .pagination .disabled {{ color: #ccc; border-color: #ccc; cursor: not-allowed; }}
          .pagination .disabled:hover {{ background: transparent; color: #ccc; }}
          @media(max-width: 600px) {{ table, th, td {{ font-size: 14px; }} }}
        </style>
      </head>
      <body>
        <h1>📊 Collected Emails</h1>
        <div class="filters">
          <form method="get" action="/dashboard">
            <div>
              <label for="date_filter">Date</label><br>
              <select name="date_filter" id="date_filter">
                <option value="" {"selected" if not date_filter else ""}>All time</option>
                <option value="today" {"selected" if date_filter=="today" else ""}>Today</option>
                <option value="yesterday" {"selected" if date_filter=="yesterday" else ""}>Yesterday</option>
                <option value="last7" {"selected" if date_filter=="last7" else ""}>Last 7 days</option>
                <option value="last30" {"selected" if date_filter=="last30" else ""}>Last 30 days</option>
                <option value="thisMonth" {"selected" if date_filter=="thisMonth" else ""}>This month</option>
                <option value="prevMonth" {"selected" if date_filter=="prevMonth" else ""}>Previous month</option>
                <option value="custom" {"selected" if date_filter=="custom" else ""}>Custom range</option>
              </select>
            </div>
            <div>
              <label for="start_date">Start</label><br>
              <input type="date" name="start_date" id="start_date" value="{start_date_str or ''}">
            </div>
            <div>
              <label for="end_date">End</label><br>
              <input type="date" name="end_date" id="end_date" value="{end_date_str or ''}">
            </div>
            <div>
              <input type="hidden" name="page" value="1">
              <button type="submit">Apply</button>
            </div>
          </form>
          <div style="margin-top:8px;color:#666;font-size:13px;">Range: {range_label}</div>
        </div>
        <div class="pagination-info">
          Showing {len(rows)} of {total_count} emails (Page {page} of {total_pages})
        </div>
        <table>
          <tr><th>Email</th><th>Created At</th></tr>
    """
    for email, created_at in rows:
        html += f"<tr><td>{email}</td><td>{created_at.date()}</td></tr>"

    # Add pagination controls
    html += """
        </table>
        <div class="pagination">
    """
    
    # Previous button
    if has_prev:
        html += f'<a href="/dashboard?page={page-1}{filter_qs}">« Previous</a>'
    else:
        html += '<span class="disabled">« Previous</span>'
    
    # Page numbers (show up to 5 pages around current page)
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    
    if start_page > 1:
        html += f'<a href="/dashboard?page=1{filter_qs}">1</a>'
        if start_page > 2:
            html += '<span>...</span>'
    
    for p in range(start_page, end_page + 1):
        if p == page:
            html += f'<span class="current">{p}</span>'
        else:
            html += f'<a href="/dashboard?page={p}{filter_qs}">{p}</a>'
    
    if end_page < total_pages:
        if end_page < total_pages - 1:
            html += '<span>...</span>'
        html += f'<a href="/dashboard?page={total_pages}{filter_qs}">{total_pages}</a>'
    
    # Next button
    if has_next:
        html += f'<a href="/dashboard?page={page+1}{filter_qs}">Next »</a>'
    else:
        html += '<span class="disabled">Next »</span>'
    
    html += """
        </div>
        <div class="buttons">
            <form method="get" action="/dashboard/export" style="display:inline-block;margin:10px;">
                <input type="hidden" name="date_filter" value="{date_filter or ''}">
                <input type="hidden" name="start_date" value="{start_date_str or ''}">
                <input type="hidden" name="end_date" value="{end_date_str or ''}">
                <label style="margin-right:6px;">Format:</label>
                <label><input type="radio" name="format" value="csv" checked> CSV</label>
                <label><input type="radio" name="format" value="xlsx"> XLSX</label>
                <label><input type="radio" name="format" value="pdf"> PDF</label>
                <button class="download" type="submit">Download</button>
            </form>
            <a href="/dashboard/logout" class="logout">Logout</a>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

# ==== Dashboard Logout ====
@app.get("/dashboard/logout")
async def dashboard_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/dashboard")

# ==== Export by Date and Format ====
@app.get("/dashboard/export")
async def export_data(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse("/dashboard")

    qp = request.query_params
    fmt = (qp.get("format") or "csv").lower()
    date_filter = qp.get("date_filter")
    start_date_str = qp.get("start_date")
    end_date_str = qp.get("end_date")

    start_dt, end_dt, _ = _compute_date_range(date_filter, start_date_str, end_date_str)

    conn = get_connection()
    cur = conn.cursor()
    params: List = []
    where_sql = ""
    if start_dt and end_dt:
        where_sql = "WHERE created_at BETWEEN %s AND %s"
        params.extend([start_dt, end_dt])
    cur.execute(
        f"SELECT email, created_at FROM trial_emails {where_sql} ORDER BY created_at DESC",
        params,
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # CSV
    if fmt == "csv":
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(["Email", "Created At"])
        for email, created_at in rows:
            writer.writerow([email, created_at.date()])
        csv_file.seek(0)
        fname = "emails.csv"
        if start_dt and end_dt:
            fname = f"emails_{start_dt.date().isoformat()}_{end_dt.date().isoformat()}.csv"
        return StreamingResponse(
            csv_file,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={fname}"},
        )

    # XLSX
    if fmt == "xlsx":
        if Workbook is None:
            return JSONResponse({"error": "XLSX export requires openpyxl to be installed"}, status_code=500)
        wb = Workbook()
        ws = wb.active
        ws.title = "Emails"
        ws.append(["Email", "Created At"])
        for email, created_at in rows:
            ws.append([email, created_at.date().isoformat()])
        bio = BytesIO()
        wb.save(bio)
        bio.seek(0)
        fname = "emails.xlsx"
        if start_dt and end_dt:
            fname = f"emails_{start_dt.date().isoformat()}_{end_dt.date().isoformat()}.xlsx"
        return StreamingResponse(
            bio,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={fname}"},
        )

    # PDF
    if fmt == "pdf":
        if SimpleDocTemplate is None:
            return JSONResponse({"error": "PDF export requires reportlab to be installed"}, status_code=500)
        bio = BytesIO()
        doc = SimpleDocTemplate(bio, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        title = Paragraph("Collected Emails", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))
        data = [["Email", "Created At"]] + [[e, c.date().isoformat()] for e, c in rows]
        table = Table(data, colWidths=[350, 150])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#f2f2f2")]),
            ])
        )
        elements.append(table)
        doc.build(elements)
        bio.seek(0)
        fname = "emails.pdf"
        if start_dt and end_dt:
            fname = f"emails_{start_dt.date().isoformat()}_{end_dt.date().isoformat()}.pdf"
        return StreamingResponse(
            bio,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={fname}"},
        )

    return JSONResponse({"error": "Unsupported format"}, status_code=400)
