from typing import Any

from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import escape
from django.middleware.csrf import get_token

from . import data


# CSRF - Cross-Site Request Forgery
def _csrf_field(request: HttpRequest) -> str:
    token = get_token(request)

    return (
        f"""
        <input type='hidden' 
        name='csrfmiddlewaretoken'
        value='{escape(token)}'>
"""
    )


def _html_shell(title: str, body: str) -> str:
    safe_title = escape(title)

    return f"""
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{safe_title} | Knowledge Hub</title>

    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-light: #eef2ff;

            --background: #f8fafc;
            --surface: #ffffff;

            --text: #0f172a;
            --text-secondary: #64748b;

            --border: #e2e8f0;

            --radius: 14px;

            --shadow:
                0 1px 2px rgba(15, 23, 42, 0.04),
                0 8px 24px rgba(15, 23, 42, 0.06);
        }}

        body {{
            min-height: 100vh;

            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            background: var(--background);
            color: var(--text);

            line-height: 1.6;
        }}


        /* =========================
           NAVBAR
        ========================= */

        nav {{
            height: 64px;

            display: flex;
            align-items: center;
            gap: 8px;

            padding: 0 max(24px, calc((100% - 1000px) / 2));

            background: rgba(255, 255, 255, 0.9);

            border-bottom: 1px solid var(--border);

            position: sticky;
            top: 0;
            z-index: 100;

            backdrop-filter: blur(12px);
        }}

        nav a {{
            display: inline-flex;
            align-items: center;

            padding: 8px 14px;

            color: #475569;
            text-decoration: none;

            font-size: 14px;
            font-weight: 500;

            border-radius: 9px;

            transition:
                background-color 0.2s ease,
                color 0.2s ease;
        }}

        nav a:hover {{
            background: var(--primary-light);
            color: var(--primary-dark);
        }}


        /* =========================
           MAIN
        ========================= */

        main {{
            width: min(1000px, calc(100% - 40px));

            margin: 60px auto;
        }}

        .card {{
            background: var(--surface);

            border: 1px solid var(--border);
            border-radius: var(--radius);

            padding: 32px;

            box-shadow: var(--shadow);
        }}

        h1 {{
            margin-bottom: 12px;

            font-size: clamp(28px, 4vw, 40px);
            line-height: 1.2;

            letter-spacing: -0.03em;

            color: var(--text);
        }}

        p {{
            margin: 10px 0;

            color: var(--text-secondary);
        }}


        /* =========================
           LINKS
        ========================= */

        main a {{
            color: var(--primary-dark);
            font-weight: 500;
            text-decoration: none;
        }}

        main a:hover {{
            text-decoration: underline;
        }}


        /* =========================
           NOTES LIST
        ========================= */

        ul {{
            list-style: none;

            display: grid;
            gap: 12px;

            margin: 28px 0;
        }}

        li {{
            background: var(--surface);

            border: 1px solid var(--border);
            border-radius: 12px;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease;
        }}

        li:hover {{
            transform: translateY(-2px);

            border-color: #c7d2fe;

            box-shadow:
                0 8px 24px rgba(15, 23, 42, 0.07);
        }}

        li a {{
            display: block;

            padding: 18px 20px;

            color: var(--text);

            font-weight: 600;

            text-decoration: none;
        }}

        li a:hover {{
            color: var(--primary-dark);
            text-decoration: none;
        }}

        .tag {{
            display: inline-block;

            margin-left: 8px;

            color: #818cf8;

            font-size: 13px;
            font-weight: 500;
        }}


        /* =========================
           BUTTON
        ========================= */

        .button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;

            margin-top: 20px;

            padding: 10px 16px;

            background: var(--primary);

            color: white !important;

            border-radius: 10px;

            text-decoration: none !important;

            font-size: 14px;
            font-weight: 600;

            transition:
                background-color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }}

        .button:hover {{
            background: var(--primary-dark);

            transform: translateY(-1px);

            box-shadow:
                0 6px 16px rgba(79, 70, 229, 0.18);
        }}


        /* =========================
           NOTE DETAIL
        ========================= */

        .note-info {{
            display: grid;
            gap: 14px;

            margin-top: 24px;
        }}

        .note-info p {{
            margin: 0;

            padding: 14px 16px;

            background: #f8fafc;

            border: 1px solid var(--border);
            border-radius: 10px;

            color: #475569;
        }}

        .note-info strong {{
            color: var(--text);
        }}


        /* =========================
           CREATE FORM
        ========================= */

        .form-description {{
            margin-top: -2px;
            margin-bottom: 28px;

            color: var(--text-secondary);

            font-size: 15px;
        }}

        .note-form {{
            margin-top: 25px;
        }}

        .form-group {{
            margin-bottom: 22px;
        }}

        .form-group label {{
            display: block;

            margin-bottom: 8px;

            color: var(--text);

            font-size: 14px;
            font-weight: 600;
        }}

        .form-group input,
        .form-group textarea {{
            width: 100%;

            padding: 12px 14px;

            font-family: inherit;
            font-size: 15px;

            color: var(--text);

            background: #ffffff;

            border: 1px solid var(--border);
            border-radius: 10px;

            outline: none;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease,
                background-color 0.2s ease;
        }}

        .form-group textarea {{
            min-height: 160px;

            resize: vertical;

            line-height: 1.6;
        }}

        .form-group input::placeholder,
        .form-group textarea::placeholder {{
            color: #94a3b8;
        }}

        .form-group input:hover,
        .form-group textarea:hover {{
            border-color: #cbd5e1;
        }}

        .form-group input:focus,
        .form-group textarea:focus {{
            border-color: var(--primary);

            background: #ffffff;

            box-shadow:
                0 0 0 3px rgba(99, 102, 241, 0.12);
        }}


        /* =========================
           FORM ACTIONS
        ========================= */

        .form-actions {{
            display: flex;
            align-items: center;
            gap: 12px;

            margin-top: 30px;
            padding-top: 24px;

            border-top: 1px solid var(--border);
        }}

        .submit-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;

            padding: 11px 20px;

            background: var(--primary);
            color: #ffffff;

            border: none;
            border-radius: 10px;

            font-family: inherit;
            font-size: 14px;
            font-weight: 600;

            cursor: pointer;

            transition:
                background-color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }}

        .submit-button:hover {{
            background: var(--primary-dark);

            transform: translateY(-1px);

            box-shadow:
                0 6px 16px rgba(79, 70, 229, 0.2);
        }}

        .submit-button:active {{
            transform: translateY(0);
        }}

        .cancel-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;

            padding: 10px 16px;

            color: #475569 !important;

            background: #ffffff;

            border: 1px solid var(--border);
            border-radius: 10px;

            font-size: 14px;
            font-weight: 600;

            text-decoration: none !important;

            transition:
                background-color 0.2s ease,
                border-color 0.2s ease,
                color 0.2s ease;
        }}

        .cancel-button:hover {{
            background: #f8fafc;

            border-color: #cbd5e1;

            color: var(--text) !important;
        }}


        /* =========================
           RESPONSIVE
        ========================= */

        @media (max-width: 600px) {{

            nav {{
                height: auto;

                padding: 12px 16px;

                overflow-x: auto;
            }}

            nav a {{
                white-space: nowrap;
            }}

            main {{
                width: calc(100% - 28px);

                margin: 32px auto;
            }}

            .card {{
                padding: 22px;
            }}

            h1 {{
                font-size: 28px;
            }}

            .form-actions {{
                flex-direction: column;

                align-items: stretch;
            }}

            .submit-button,
            .cancel-button {{
                width: 100%;
            }}
        }}

    </style>
</head>

<body>

    <nav>
        <a href="{escape(reverse('home'))}">
            Ana səhifə
        </a>

        <a href="{escape(reverse('about'))}">
            Haqqında
        </a>

        <a href="{escape(reverse('notes_list'))}">
            Qeydlər
        </a>
    </nav>


    <main>
        <div class="card">
            {body}
        </div>
    </main>

</body>
</html>
"""


def home(request: HttpRequest) -> HttpResponse:
    body = f"""
        <h1>Knowledge Hub</h1>

        <p>
            Knowledge Hub layihəsinə xoş gəlmisiniz.
        </p>

        <p>
            Qeydlərinizi bir yerdə saxlayın və rahat şəkildə idarə edin.
        </p>

        <a
            class="button"
            href="{escape(reverse('notes_list'))}"
        >
            Qeydlər siyahısına keç →
        </a>
    """

    return HttpResponse(
        _html_shell("Ana Səhifə", body)
    )


def about(request: HttpRequest) -> HttpResponse:
    body = """
        <h1>Knowledge Hub layihəsi haqqında</h1>

        <p>
            Bu layihədə öz qeydlərinizi yarada və idarə edə bilərsiniz.
        </p>

        <p>
            Qeydləri kateqoriya və tag-lərə əsasən təşkil etmək mümkündür.
        </p>
    """

    return HttpResponse(
        _html_shell("Haqqında", body)
    )


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get('tag')
    raw_category = request.GET.get('category')

    items: list[str] = []

    notes: list[dict[str, Any]] = data.list_notes()

    if raw_tag:
        tag_filter = raw_tag.strip()

        notes = [
            n for n in notes
            if n['tag'] == tag_filter
        ]

    if raw_category:
        category_filter = raw_category.strip()

        notes = [
            n for n in notes
            if n['category'] == category_filter
        ]

    for note in notes:
        url = reverse(
            'note_detail',
            kwargs={"note_id": note['id']}
        )

        items.append(
            f"""
            <li>
                <a href="{escape(url)}">

                    {escape(note['title'])}

                    <span class="tag">
                        #{escape(note['tag'])}
                    </span>

                </a>
            </li>
            """
        )

    body = f"""
        <h1>Knowledge Hub Notes</h1>

        <p>
            Bütün qeydləriniz
        </p>

        <ul>
            {''.join(items)}
        </ul>

        <a
            class="button"
            href="{escape(reverse('home'))}"
        >
            ← Ana səhifəyə qayıt
        </a>
    """

    return HttpResponse(
        _html_shell("Qeydlər", body)
    )


def note_detail(
    request: HttpRequest,
    note_id: int
) -> HttpResponse:

    note = data.get_note(note_id)

    if note is None:
        return HttpResponse(
            f"Note id={note_id} not found"
        )

    body = f"""
        <h1>
            {escape(note['title'])}
        </h1>

        <div class="note-info">

            <p>
                <strong>Mətn</strong>
                <br>

                {escape(note['body'])}
            </p>

            <p>
                <strong>Tag</strong>
                <br>

                #{escape(note['tag'])}
            </p>

            <p>
                <strong>Kateqoriya</strong>
                <br>

                {escape(note['category'])}
            </p>

        </div>

        <p>
            </p>
        <a
            class="button"
            href="{escape(reverse('note_edit', kwargs={'note_id': note_id}))}"
        >
            Dəyiş
        </a>
        <a
            class="button"
            href="{escape(reverse('note_delete', kwargs={'note_id': note_id}))}"
        >
            Sil
        </a>
        </p>
        <a
            class="button"
            href="{escape(reverse('notes_list'))}"
        >
            ← Qeydlər siyahısına qayıt
        </a>
    """

    return HttpResponse(
        _html_shell(note['title'], body)
    )


def note_edit(
    request: HttpRequest,
    note_id: int
) -> HttpResponse:

    note = data.get_note(note_id)

    if note is None:
        return HttpResponse(
            f"Note id={note_id} not found"
        )

    if request.method == "POST":

        title = request.POST.get("title", "")
        body = request.POST.get("body", "")
        category = request.POST.get("category", "")
        tag = request.POST.get("tag", "")

        data.update_note(
            note_id=note_id,
            title=title,
            body=body,
            category=category or "qarışıq",
            tag=tag or None
        )

        return redirect(
            reverse(
                "note_detail",
                kwargs={"note_id": note_id}
            )
        )

    form = f"""
        <h1>Qeydi dəyiş</h1>

        <p class="form-description">
            Qeydin məlumatlarını dəyişdirin.
        </p>

        <form
            method="post"
            class="note-form"
        >

            {_csrf_field(request)}

            <div class="form-group">
                <label for="title">
                    Ad
                </label>

                <input
                    id="title"
                    type="text"
                    name="title"
                    value="{escape(note['title'])}"
                    placeholder="Qeydin adını daxil edin"
                >
            </div>

            <div class="form-group">
                <label for="body">
                    Mətn
                </label>

                <textarea
                    id="body"
                    name="body"
                    rows="6"
                    placeholder="Qeydinizin mətnini bura yazın"
                >{escape(note['body'])}</textarea>
            </div>

            <div class="form-group">
                <label for="tag">
                    Tag
                </label>

                <input
                    id="tag"
                    type="text"
                    name="tag"
                    value="{escape(note['tag'] or '')}"
                    placeholder="Məsələn: django"
                >
            </div>

            <div class="form-group">
                <label for="category">
                    Kateqoriya
                </label>

                <input
                    id="category"
                    type="text"
                    name="category"
                    value="{escape(note['category'])}"
                    placeholder="Məsələn: Backend"
                >
            </div>

            <div class="form-actions">

                <button
                    type="submit"
                    class="submit-button"
                >
                    Yadda saxla
                </button>

                <a
                    href="{escape(reverse(
                        'note_detail',
                        kwargs={'note_id': note_id}
                    ))}"
                    class="cancel-button"
                >
                    Ləğv et
                </a>

            </div>

        </form>
    """

    return HttpResponse(
        _html_shell(
            f"Qeydi dəyiş - {note['title']}",
            form
        )
    )


def note_delete(
    request: HttpRequest,
    note_id: int
) -> HttpResponse:

    note = data.get_note(note_id)

    if note is None:
        return HttpResponse(
            f"Note id={note_id} not found"
        )

    if request.method == "POST":

        data.delete_note(note_id)

        return redirect(
            reverse("notes_list")
        )

    body = f"""
        <h1>Qeydi sil</h1>

        <p>
            <strong>{escape(note['title'])}</strong>
            qeydini silmək istədiyinizə əminsiniz?
        </p>

        <form method="post" class="note-form">

            {_csrf_field(request)}

            <div class="form-actions">

                <button
                    type="submit"
                    class="submit-button"
                >
                    Bəli, sil
                </button>

                <a
                    href="{escape(reverse(
                        'note_detail',
                        kwargs={'note_id': note_id}
                    ))}"
                    class="cancel-button"
                >
                    Ləğv et
                </a>

            </div>

        </form>
    """

    return HttpResponse(
        _html_shell(
            "Qeydi sil",
            body
        )
    )

def note_create(request: HttpRequest) -> HttpResponse:
    title_val = ''
    body_val = ''
    category_val = ''
    tag_val = ''

    if request.method == 'POST':

        title = request.POST.get('title', "")
        body = request.POST.get('body', "")
        category = request.POST.get('category', "")
        tag = request.POST.get('tag')

        if not title.strip():
            title_val = escape(title)
            body_val = escape(body)
            category_val = escape(category)
            tag_val = escape(tag or '')

            form = f"""
                <h1>Yeni qeyd yarat</h1>

                <p class="form-description">
                    Ad boş ola bilməz.
                </p>

                <form method="post" class="note-form">

                    {_csrf_field(request)}

                    <div class="form-group">
                        <label for="title">Ad</label>

                        <input
                            id="title"
                            type="text"
                            name="title"
                            value="{title_val}"
                            placeholder="Qeydin adını daxil edin"
                        >
                    </div>

                    <div class="form-group">
                        <label for="body">Mətn</label>

                        <textarea
                            id="body"
                            name="body"
                            rows="6"
                            placeholder="Qeydinizin mətnini bura yazın"
                        >{body_val}</textarea>
                    </div>

                    <div class="form-group">
                        <label for="tag">Tag</label>

                        <input
                            id="tag"
                            type="text"
                            name="tag"
                            value="{tag_val}"
                            placeholder="Məsələn: django"
                        >
                    </div>

                    <div class="form-group">
                        <label for="category">Kateqoriya</label>

                        <input
                            id="category"
                            type="text"
                            name="category"
                            value="{category_val}"
                            placeholder="Məsələn: Backend"
                        >
                    </div>

                    <div class="form-actions">

                        <button
                            type="submit"
                            class="submit-button"
                        >
                            Qeyd yarat
                        </button>

                        <a
                            href="{escape(reverse('notes_list'))}"
                            class="cancel-button"
                        >
                            Ləğv et
                        </a>

                    </div>

                </form>
            """

            return HttpResponse(
                _html_shell("Qeyd yarat", form)
            )

        data.create_note(
            title=title,
            body=body,
            category=category or "qarışıq",
            tag=tag or None
        )

        return redirect(
            reverse('notes_list')
        )

    form = f"""
        <h1>Yeni qeyd yarat</h1>

        <p class="form-description">
            Yeni qeydin məlumatlarını daxil edin.
        </p>

        <form
            method="post"
            class="note-form"
        >

            {_csrf_field(request)}

            <div class="form-group">

                <label for="title">
                    Ad
                </label>

                <input
                    id="title"
                    type="text"
                    name="title"
                    value=""
                    placeholder="Qeydin adını daxil edin"
                >

            </div>

            <div class="form-group">

                <label for="body">
                    Mətn
                </label>

                <textarea
                    id="body"
                    name="body"
                    rows="6"
                    placeholder="Qeydinizin mətnini bura yazın"
                ></textarea>

            </div>

            <div class="form-group">

                <label for="tag">
                    Tag
                </label>

                <input
                    id="tag"
                    type="text"
                    name="tag"
                    value=""
                    placeholder="Məsələn: django"
                >

            </div>

            <div class="form-group">

                <label for="category">
                    Kateqoriya
                </label>

                <input
                    id="category"
                    type="text"
                    name="category"
                    value=""
                    placeholder="Məsələn: Backend"
                >

            </div>

            <div class="form-actions">

                <button
                    type="submit"
                    class="submit-button"
                >
                    Qeyd yarat
                </button>

                <a
                    href="{escape(reverse('notes_list'))}"
                    class="cancel-button"
                >
                    Ləğv et
                </a>

            </div>

        </form>
    """

    return HttpResponse(
        _html_shell(
            "Qeyd yarat",
            form
        )
    )