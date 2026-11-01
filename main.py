import csv
import io
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QPushButton,
    QStackedWidget,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QKeySequence, QShortcut
import datetime as dt

# шаблон первого окна
mainwindow = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>721</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout">
    <item row="0" column="0">
     <widget class="QTabWidget" name="tabWidget">
      <property name="currentIndex">
       <number>0</number>
      </property>
      <widget class="QWidget" name="tab">
       <attribute name="title">
        <string>Рецепты</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_2">
        <item row="0" column="0">
         <layout class="QHBoxLayout" name="horizontalLayout" stretch="1,1">
          <item>
           <widget class="QListWidget" name="recipes_list"/>
          </item>
          <item>
           <layout class="QVBoxLayout" name="elements" stretch="0,0,0,0,0">
            <item>
             <spacer name="verticalSpacer">
              <property name="orientation">
               <enum>Qt::Vertical</enum>
              </property>
              <property name="sizeHint" stdset="0">
               <size>
                <width>20</width>
                <height>40</height>
               </size>
              </property>
             </spacer>
            </item>
            <item>
             <widget class="QPushButton" name="open_Button">
              <property name="text">
               <string>Открыть</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QPushButton" name="del_Button">
              <property name="text">
               <string>Удалить</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLabel" name="label_2">
              <property name="text">
               <string>Кол-во приготовленных блюд</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QSpinBox" name="count_ready"/>
            </item>
           </layout>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="tab_2">
       <attribute name="title">
        <string>Добавить</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_3">
        <item row="0" column="0">
         <layout class="QVBoxLayout" name="verticalLayout" stretch="2,1">
          <property name="spacing">
           <number>6</number>
          </property>
          <item>
           <layout class="QVBoxLayout" name="verticalLayout_5">
            <item>
             <widget class="QLabel" name="art">
              <property name="text">
               <string/>
              </property>
             </widget>
            </item>
           </layout>
          </item>
          <item>
           <layout class="QVBoxLayout" name="verticalLayout_6">
            <item>
             <widget class="QPushButton" name="addButton">
              <property name="text">
               <string>Добавить</string>
              </property>
             </widget>
            </item>
           </layout>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="tab_3">
       <attribute name="title">
        <string>Таймер</string>
       </attribute>
       <layout class="QGridLayout" name="gridLayout_4">
        <item row="0" column="0">
         <layout class="QVBoxLayout" name="verticalLayout_2" stretch="7,5,0,0,0">
          <item>
           <widget class="QLCDNumber" name="time"/>
          </item>
          <item>
           <widget class="QTimeEdit" name="cnt_time"/>
          </item>
          <item>
           <widget class="QPushButton" name="start_Button">
            <property name="text">
             <string>Старт</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="stop_Button">
            <property name="text">
             <string>Стоп</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QLabel" name="label">
            <property name="font">
             <font>
              <weight>75</weight>
              <italic>false</italic>
              <bold>true</bold>
              <underline>false</underline>
              <strikeout>false</strikeout>
             </font>
            </property>
            <property name="text">
             <string>часы:минуты</string>
            </property>
           </widget>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>721</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
# шаблон второго окна
recipe = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>600</width>
    <height>700</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <layout class="QGridLayout" name="gridLayout">
   <item row="0" column="0">
    <layout class="QGridLayout" name="gridLayout_2">
     <item row="0" column="0">
      <layout class="QVBoxLayout" name="verticalLayout_2" stretch="1,1,0,6">
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_2">
         <item>
          <widget class="QTextEdit" name="name">
           <property name="font">
            <font>
             <weight>75</weight>
             <bold>true</bold>
            </font>
           </property>
           <property name="html">
            <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:600; font-style:normal;&quot;&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;Введите название блюда.&lt;/p&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <spacer name="verticalSpacer_3">
         <property name="orientation">
          <enum>Qt::Vertical</enum>
         </property>
         <property name="sizeHint" stdset="0">
          <size>
           <width>20</width>
           <height>40</height>
          </size>
         </property>
        </spacer>
       </item>
       <item>
        <widget class="QLabel" name="label">
         <property name="text">
          <string>Пункты годовки.</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QStackedWidget" name="recipe">
         <property name="currentIndex">
          <number>0</number>
         </property>
         <widget class="QWidget" name="page_3"/>
         <widget class="QWidget" name="page_4"/>
        </widget>
       </item>
      </layout>
     </item>
     <item row="0" column="1">
      <widget class="Line" name="line">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
      </widget>
     </item>
     <item row="0" column="2">
      <layout class="QVBoxLayout" name="verticalLayout" stretch="0,0,0,0">
       <item>
        <spacer name="verticalSpacer">
         <property name="orientation">
          <enum>Qt::Vertical</enum>
         </property>
         <property name="sizeHint" stdset="0">
          <size>
           <width>20</width>
           <height>40</height>
          </size>
         </property>
        </spacer>
       </item>
       <item>
        <widget class="QPushButton" name="add">
         <property name="text">
          <string>Добавить</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="save_Button">
         <property name="text">
          <string>Сохранить</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QTextEdit" name="premch">
         <property name="styleSheet">
          <string notr="true">QTextEdit {background-color: transparent; border: none}</string>
         </property>
         <property name="readOnly">
          <bool>true</bool>
         </property>
         <property name="html">
          <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;Кнопка 'Добавить' добавляет пункт.&lt;/p&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;Для переключения между пунктами можно использовать &amp;quot;&amp;lt;-&amp;quot; или &amp;quot;-&amp;gt;&amp;quot;.&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
         </property>
        </widget>
       </item>
      </layout>
     </item>
    </layout>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

signal_name = []
signal_recipe = []


class Recipe(QWidget):
    """Второй класс окно. В нем можно записать новый рецепт"""

    def __init__(self):
        super().__init__()
        f = io.StringIO(recipe)
        uic.loadUi(f, self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        while self.recipe.count() > 0:
            widget = self.recipe.widget(0)
            self.recipe.removeWidget(widget)
        self.new_point()
        self.left = QShortcut(QKeySequence("Left"), self)
        self.left.activated.connect(lambda sign="-": self.moving(sign))
        self.right = QShortcut(QKeySequence("Right"), self)
        self.right.activated.connect(lambda sign="+": self.moving(sign))
        self.save_Button.clicked.connect(self.save)
        self.add.clicked.connect(self.new_point)

    # Добавление в SteckWidget пункта
    def new_point(self):
        new_widget = QWidget()
        layout = QVBoxLayout(new_widget)

        txt = QTextEdit()
        layout.addWidget(txt, 1)

        art = QLabel()
        layout.addWidget(art, 2)

        self.recipe.addWidget(new_widget)
        self.recipe.setCurrentWidget(new_widget)

    # Перемещение по SteckWidget
    def moving(self, sign):
        tot_widget = self.recipe.count()
        current_indx = self.recipe.currentIndex()
        print(current_indx)
        if sign == "-":
            current_indx = current_indx - 1
        else:
            current_indx = current_indx + 1

        if 0 <= current_indx <= tot_widget:
            self.recipe.setCurrentIndex(current_indx)

    # Перемещение курсора
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        focused_widget = self.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()

    # Сохранение
    def save(self):
        name_recipe = self.name.toPlainText().rstrip()
        if len(name_recipe) <= 2:
            self.name.setPlainText("Должно быть больше 2 символов!!!")
        else:
            signal_name.append(name_recipe)
            ...
            self.close()

    # Добавление картинки
    def addart(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Выбрать картинку",
            "",
            "Картинка (*.jpg);;Картинка (*.png);;Картинка (*.webp);",
        )[0]
        if fname:
            current_widget = self.recipe.currentWidget()
            label_widget = current_widget.findChild(QLabel)
            pixmap = QPixmap(fname)
            scaled_pixmap = pixmap.scaled(
                350,
                350,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            label_widget.setPixmap(scaled_pixmap)


class Save_csv:
    """Класс сохранения в csv файл"""

    def __init__(self):
        pass

    # Подготовка данных
    def write_csv(self, cnt_ready, count_recipes, time):
        self.cnt_ready = cnt_ready
        self.count_recipes = count_recipes
        hour = time.total_seconds() // 3600
        minutes = (time.total_seconds() // 60) % 60
        sec = time.total_seconds()
        self.time = f"{hour}:{minutes}:{sec}"
        with open("count.csv", "r", encoding="utf8") as f:
            read = csv.reader(f, delimiter=",")
            head = next(read, False)
            if head:
                for row in read:
                    old_hour, old_minuets, old_sec = row[2].split(":")
                    old_hour, old_minuets, old_sec = (
                        int(old_hour),
                        int(old_minuets),
                        float(old_sec),
                    )
                    hour += old_hour
                    minutes += old_minuets
                    sec += old_sec
                    if sec > 60:
                        minutes += (sec) // 60
                        sec = (sec) % 60
                    if minutes > 60:
                        hour += (minutes) // 60
                        minutes = (minutes) % 60
                    self.time = f"{int(float(hour))}:{int(float(minutes))}:{sec}"
        self.save()

    # Загруска файда csv в программу
    def load_open(self):
        with open("count.csv", "r", encoding="utf8") as f:
            read = csv.reader(f, delimiter=",")
            next(f)
            for row in read:
                hour, minutes, sec = row[2].split(":")
                total_hour = int(hour)
                return row[0], total_hour

    # Сохранение в csv
    def save(self):
        with open("count.csv", "w", encoding="utf8") as f:
            f.write("count_ready,count_recipes,max_time\n")
            f.write(f"{self.cnt_ready}, {self.count_recipes}, {self.time}")


class Main(QMainWindow):
    """Главны класс. В нем можно довбавлять, изменять, открывать, удалять рецепты."""

    def __init__(self):
        super().__init__()
        f = io.StringIO(mainwindow)
        uic.loadUi(f, self)
        self.list_window = []
        self.list_elem = QStackedWidget()
        note = QLabel("Ингредиенты")
        self.elements.insertWidget(0, self.list_elem)
        self.elements.insertWidget(0, note)
        pixmap = QPixmap("картинка на добавить.jpg")
        scaled_pixmap = pixmap.scaled(
            700,
            400,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.art.setPixmap(scaled_pixmap)
        self.time.setDigitCount(5)
        value_ready, self.total_hour = Save_csv().load_open()
        value_ready = int(value_ready)
        self.count_ready.setValue(value_ready)
        self.start_time = dt.datetime.now()

        self.addButton.clicked.connect(self.new_recipe)
        self.open_Button.clicked.connect(self.open_change)
        self.del_Button.clicked.connect(self.dele)
        self.recipes_list.currentRowChanged.connect(self.switch_page)
        self.start_Button.clicked.connect(self.start)
        self.stop_Button.setEnabled(False)
        self.stop_Button.clicked.connect(self.stop)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    # Создание второго окна
    def new_recipe(self):
        window_recipe = Recipe()
        self.list_window.append(window_recipe)
        window_recipe.destroyed.connect(lambda: self.remove(window_recipe))
        window_recipe.destroyed.connect(self.add_recipe)
        window_recipe.show()

    # Удаление окна из списка окон
    def remove(self, window_recipe):
        if window_recipe in self.list_window:
            self.list_window.remove(window_recipe)

    # Запись названия в recipes_list
    def add_recipe(self):
        if len(signal_name) != 0:
            if signal_name[0] not in [
                self.recipes_list.item(i).text()
                for i in range(self.recipes_list.count())
            ]:
                new_widget = QWidget()
                layout = QVBoxLayout(new_widget)
                txt = QTextEdit()
                layout.addWidget(txt)
                self.list_elem.addWidget(new_widget)
                self.recipes_list.addItem(signal_name[0])
                self.statusBar().showMessage(
                    f"Кол-во {len(self.recipes_list)} рецептов, кол-во часов {self.total_hour}"
                )
        signal_name.clear()

    # Перемещение по recipes_list
    def switch_page(self, index):
        self.list_elem.setCurrentIndex(index)
        count_recipes = len(self.recipes_list)
        if count_recipes % 100 == 0:
            self.statusBar().showMessage(
                f"Поздравляем у тебя целых {count_recipes} рецептов"
            )

    # Метод для старта таймера
    def start(self):
        input_time = self.cnt_time.time()
        self.dt_time = input_time
        input_time = input_time.toString("hh:mm")
        self.timer.start(60000)
        self.start_Button.setEnabled(False)
        self.stop_Button.setEnabled(True)
        self.time.display(input_time)

    # Метод обновление таймера
    def update_timer(self):
        self.dt_time = self.dt_time.addSecs(-60)
        str_time = self.dt_time.toString("hh:mm")
        self.time.display(str_time)
        if str_time == "00:00":
            self.stop()

    # Метод остоновки таймера
    def stop(self):
        self.stop_Button.setEnabled(False)
        self.start_Button.setEnabled(True)
        self.time.display("00:00")
        self.timer.stop()

    # Метод кнопки открытия второго окна
    def open_change(self):
        pass

    # Удаляет рецепт из recipes_list
    def dele(self):
        pass

    # Диалоговое окно закрытия
    def closeEvent(self, event):
        wind_question = QMessageBox.question(
            self,
            "Закрытие программы",
            "Вы уверены, что хотите выйти?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if wind_question == QMessageBox.StandardButton.Yes:
            end_time = dt.datetime.now()
            difference = end_time - self.start_time
            save = Save_csv()
            save.write_csv(self.count_ready.value(), len(self.recipes_list), difference)
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
