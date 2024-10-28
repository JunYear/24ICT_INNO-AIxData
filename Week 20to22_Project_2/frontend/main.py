import flet
from flet import (
    Page, Text, ElevatedButton, FilePicker, ProgressBar, Column, Row,
    TextField, Divider, Icon, icons, AlertDialog, SnackBar, Card, Container,
    padding, alignment, colors, AppBar, IconButton, Image, LinearGradient,
    alignment, border_radius
)
import requests

API_URL = 'http://localhost:5000/upload'

def main(page: Page):
    page.title = "IT 면접 보조 서비스"
    page.window.width = 800
    page.window.height = 600
    page.theme_mode = 'light'  # 또는 'dark'로 설정 가능

    # 컬러 팔레트 설정
    primary_color = colors.BLUE
    secondary_color = colors.WHITE

    # 헤더 영역 (AppBar)
    page.appbar = AppBar(
        title=Text("AI기반 IT 면접 보조 서비스", color=colors.WHITE),
        center_title=True,
        bgcolor=primary_color,
    )

    # 상태 메시지 표시용 스낵바
    def show_message(message):
        snack_bar = SnackBar(
            content=Text(message),
            bgcolor=colors.GREEN
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # 오류 메시지 표시용 다이얼로그
    def show_error(message):
        def close_dialog(e):
            error_dialog.open = False
            page.update()

        error_dialog = AlertDialog(
            title=Text("오류", weight="bold"),
            content=Text(message),
            actions=[ElevatedButton("확인", on_click=close_dialog)],
            on_dismiss=lambda e: setattr(error_dialog, 'open', False)
        )
        # 다이얼로그를 page.overlay에 추가
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()

    def on_upload_result(e):
        if e.files:
            selected_file.value = e.files[0].name
            file_path.value = e.files[0].path
            upload_button.disabled = False
            page.update()

    def upload_file(e):
        if file_path.value:
            upload_button.disabled = True
            progress_bar.visible = True
            progress_bar.value = None
            page.update()

            try:
                files = {'file': open(file_path.value, 'rb')}
                response = requests.post(API_URL, files=files)
                if response.status_code == 200:
                    data = response.json()
                    transcript.value = data.get('text', '')
                    feedback_summary.value = data.get('feedback', {}).get('summary', '')
                    # 세부 피드백 표시
                    feedback_details.controls = [
                        Text(f"문장 수: {data.get('feedback', {}).get('sentence_count', '')}"),
                        Text(f"단어 수: {data.get('feedback', {}).get('word_count', '')}"),
                        Text(f"키워드: {', '.join(data.get('feedback', {}).get('keywords', []))}"),
                    ]
                    # 결과 섹션 표시
                    result_section.visible = True
                    show_message("분석이 완료되었습니다.")
                else:
                    show_error("분석 중 오류가 발생했습니다.")
            except Exception as ex:
                show_error(f"오류가 발생했습니다: {ex}")
            finally:
                progress_bar.visible = False
                upload_button.disabled = False
                page.update()

    selected_file = TextField(label="선택된 파일", read_only=True, expand=True)
    file_path = TextField(visible=False)

    pick_files_dialog = FilePicker(on_result=on_upload_result)
    page.overlay.append(pick_files_dialog)

    select_button = ElevatedButton(
        "음성 파일 선택",
        icon=icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False)
    )
    upload_button = ElevatedButton(
        "업로드 및 분석",
        icon=icons.ANALYTICS,
        on_click=upload_file,
        disabled=True
    )
    progress_bar = ProgressBar(width=800, visible=False)

    # 결과 섹션 (초기에는 숨김)
    transcript = Text(value='', selectable=True)
    feedback_summary = Text(value='', weight='bold')
    feedback_details = Column([])

    result_section = Column(
        [
            Divider(),
            Text("인식된 텍스트:", size=18, weight='bold'),
            Card(
                content=Container(
                    content=transcript,
                    padding=padding.all(10),
                    bgcolor=colors.LIGHT_BLUE_50,
                    border_radius=border_radius.all(5),
                ),
                elevation=2,
            ),
            Divider(),
            Text("피드백:", size=18, weight='bold'),
            Card(
                content=Container(
                    content=Column([
                        feedback_summary,
                        Divider(),
                        feedback_details,
                    ]),
                    padding=padding.all(10),
                    bgcolor=colors.GREEN_50,
                    border_radius=border_radius.all(5),
                ),
                elevation=2,
            ),
        ],
        visible=False
    )

    # 메인 컨텐츠 구성
    page.add(
        Column(
            [
                # 헤더 이미지 또는 로고 추가 가능
                # Image(src="assets/logo.png", width=100, height=100),
                Row(
                    [selected_file, select_button, upload_button],
                    alignment="center",
                    vertical_alignment="center",
                ),
                progress_bar,
                result_section,
            ],
            horizontal_alignment="center",
            scroll='auto',
            expand=True,
        )
    )

flet.app(target=main)
