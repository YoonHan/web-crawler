import sys
from crawler import Crawler
from fake_useragent import UserAgent
from PySide6.QtCore import QCoreApplication, Slot, Qt
from PySide6.QtWidgets import QPushButton, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTextBrowser


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.result_text_area = QTextBrowser()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Crawler Test')
        self.setGeometry(500, 150, 600, 800)

        # Button 생성
        crawl_btn = QPushButton('크롤링 시작', self)
        crawl_btn.clicked.connect(self.start_crawl)
        quit_btn = QPushButton('종료', self)
        quit_btn.clicked.connect(QCoreApplication.instance().quit)

        # TextEdit
        self.result_text_area.setReadOnly(True)
        self.result_text_area.setOpenExternalLinks(True)
        self.result_text_area.setFixedHeight(700)

        # 레이아웃 생성
        vbox = QVBoxLayout()
        vbox.addWidget(crawl_btn)
        vbox.addWidget(quit_btn)
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self.result_text_area)

        vbox.addLayout(hbox)

        # 레이아웃 window에 달기
        self.setLayout(vbox)

        # GUI window 표시
        self.show()


    @Slot()
    def start_crawl(self):
        crawler = Crawler()
        user_agent = UserAgent()
        raw_html = crawler.get_html_text(url="https://news.naver.com/", headers={'User-Agent': user_agent.random})
        parsed_html = crawler.parse_html(raw_html)
        articles_dict = {}

        sections = parsed_html.select('.main_content_inner > .main_component')
        for article_section in sections:
            title = article_section.select_one('.com_header > h4')
            if title and '헤드라인' in title.text:
                article_links = article_section.select('.hdline_news ul li a.lnk_hdline_article')
                articles_dict[title.text] = article_links
            elif title:
                article_links = article_section.select('.com_list ul li a')
                articles_dict[title.text] = article_links

        for section_name, articles in articles_dict.items():
            self.result_text_area.append(f'<strong style="color: red;">{section_name}</strong>')
            for article in articles:
                text = article.text.strip()
                self.result_text_area.append(f"{text} \t\t <a href='{article['href']}'>링크</a>")
            self.result_text_area.append('\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    app.exec_()