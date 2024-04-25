from kivy.config import Config
Config.set('kivy', 'window_icon', r'C:\Users\lanza\Desktop\Shoplist\Examples\logo.png')

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from kivy.lang import Builder
import uuid
import csv
import re



class ShoppingListManager:
    def __init__(self):
        self.category_items = {}

    def add_item(self, article, quantity, price_per_unit, category):
        try:
            quantity = float(quantity)
            price_per_unit = float(price_per_unit)
            if quantity <= 0 or price_per_unit <= 0:
                raise ValueError("La cantidad y el precio deben ser números positivos")
        except ValueError as e:
            raise ValueError("Ingrese valores numéricos válidos")

        total_price = quantity * price_per_unit
        formatted_price = "{:,.2f}".format(total_price)

        article_id = str(uuid.uuid4())
        item = {
            "id": article_id,
            "article": article,
            "quantity": quantity,
            "price_per_unit": price_per_unit,
        }

        checkbox = MDCheckbox(active=True, size_hint_x=None, width=45)
        item["checkbox"] = checkbox

        if category not in self.category_items:
            self.category_items[category] = []
        self.category_items[category].append(item)

        return item, formatted_price

    def delete_item(self, article_id):
        for category, items in self.category_items.items():
            for item in items:
                if item["id"] == article_id:
                    items.remove(item)
                    return

    def export_list(self, selected_items, file_path):
        try:
            total_price = sum(item["quantity"] * item["price_per_unit"] for item in selected_items)
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Artículo", "Cantidad", "Precio"])
                for item in selected_items:
                    article = item["article"]
                    quantity = item["quantity"]
                    price_per_unit = item["price_per_unit"]
                    csv_writer.writerow([article, quantity, price_per_unit])
                csv_writer.writerow(["Total", "", total_price])
            return True
        except Exception as e:
            raise Exception("Error al exportar la lista:", e)


class ShopperApp(MDApp):
    article_input = None
    quantity_input = None
    price_input = None
    category_spinner = None

    # Define la lista de categorías personalizadas
    categorias = ['Frutas y verduras', 'Lácteos', 'Carne y pescado', 'Cereales y derivados', 'Bebidas', 'Sin gluten', 'Vegano', 'Snacks']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Light"
        self.shopping_list_manager = ShoppingListManager()
        self.total_label = Label()

    def build(self):
        # Establecer el icono de la aplicación
        Window.set_icon('icono.ico')
        
        # Cargar el archivo KV
        root = Builder.load_file("shopper.kv")
        
        # Asignar los widgets de entrada a los atributos de la clase
        self.article_input = root.ids.article_input
        self.quantity_input = root.ids.quantity_input
        self.price_input = root.ids.price_input
        self.category_spinner = root.ids.category_spinner
        
        # Asignar self.list_layout después de cargar el archivo KV
        self.list_layout = root.ids.list_layout
        
        return root


    def add_item(self, instance, article_input, quantity_input, price_input, category_spinner):
        article = article_input.text.strip()
        quantity = quantity_input.text.strip()
        price_per_unit = price_input.text.strip()
        category = category_spinner.text
    
        try:
            item, formatted_price = self.shopping_list_manager.add_item(article, quantity, price_per_unit, category)

            if "checkbox" not in item:
                checkbox = MDCheckbox(active=True, size_hint_x=None, width=45)
                item["checkbox"] = checkbox
            else:
                checkbox = item["checkbox"]

            item_container = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=65)
            item_container.add_widget(ThreeLineListItem(text=article, secondary_text=f"Cantidad: {quantity}", tertiary_text=f"Precio: €{formatted_price}"))
            item_container.add_widget(checkbox)
            item_container.add_widget(MDIconButton(icon="delete", on_release=lambda x, i=item["id"]: self.delete_item(i)))
            item_container.article_id = item["id"]

            # Agregar el artículo al layout de la categoría correspondiente
            category_layout = self.find_or_create_category_layout(category)
            category_layout.add_widget(item_container)

            self.update_total()
            self.clear_inputs()
        except ValueError as e:
            self.show_error_dialog(str(e))

    def find_or_create_category_layout(self, category):
        # Verificar si ya existe un layout para la categoría
        for child in self.list_layout.children:
            if isinstance(child, GridLayout) and child.id == category:
                return child
        # Si no existe, crear un nuevo layout para la categoría
        category_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        category_layout.bind(minimum_height=category_layout.setter('height'))
        category_layout.id = category
        
        # Añadir el texto de la categoría con el color adecuado según el tema
        category_label = Label(text=category, font_size=18, bold=True, size_hint_y=None, height=30)
        if self.theme_cls.theme_style == "Dark":
            category_label.color = (1, 1, 1, 1)  # Establecer el color del texto en blanco en modo oscuro
        else:
            category_label.color = (0, 0, 0, 1)  # Establecer el color del texto en negro en modo claro
        
        self.list_layout.add_widget(category_label)
        self.list_layout.add_widget(category_layout)
        return category_layout
                
    def delete_item(self, article_id):
        # Buscar y eliminar el artículo solo si el checkbox está activado
        for category, items in self.shopping_list_manager.category_items.items():
            for item in items:
                if item["id"] == article_id:
                    if not item["checkbox"].active:  # Verificar si el checkbox está activado
                        self.show_error_dialog("Debe seleccionar el elemento para eliminar.")
                        return
                    items.remove(item)
                    category_layout = self.find_or_create_category_layout(category)
                    for child in category_layout.children:
                        if hasattr(child, "article_id") and child.article_id == article_id:
                            category_layout.remove_widget(child)
                    self.update_total()
                    return

    def refresh_list(self):
        self.list_layout.clear_widgets()

        for category, items in self.shopping_list_manager.category_items.items():
            if items:  # Verificar si la lista de elementos no está vacía
                category_layout = self.find_or_create_category_layout(category)  # Encontrar o crear el layout de la categoría
                category_layout.clear_widgets()  # Borrar todos los widgets existentes en el layout de la categoría

                # Agregar el texto de la categoría al layout (solo una vez)
                category_label = Label(text=category, font_size=18, bold=True, size_hint_y=None, height=30)
                category_layout.add_widget(category_label)

                # Agregar los widgets de los artículos al layout de la categoría
                for item in items:
                    article = item["article"]
                    quantity = item["quantity"]
                    price_per_unit = item["price_per_unit"]
                    total_price = quantity * price_per_unit
                    formatted_price = "{:,.2f}".format(total_price)

                    checkbox = MDCheckbox(active=True, size_hint_x=None, width=45)  # Crear un nuevo checkbox
                    item["checkbox"] = checkbox  # Actualizar el checkbox en el diccionario del artículo

                    item_container = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=65)
                    item_container.add_widget(ThreeLineListItem(text=article, secondary_text=f"Cantidad: {quantity}", tertiary_text=f"Precio: €{formatted_price}"))
                    item_container.add_widget(checkbox)  # Agregar el nuevo checkbox
                    delete_button = MDIconButton(icon="delete", on_release=lambda x, i=item["id"]: self.delete_item(i))
                    item_container.add_widget(delete_button)

                    # Agregar el contenedor del artículo al layout de la categoría
                    category_layout.add_widget(item_container)
            else:
                # Si la lista de elementos está vacía, no agregar el texto de la categoría
                pass
    


    def update_total(self):
        total_price = sum(item["quantity"] * item["price_per_unit"] for category, items in self.shopping_list_manager.category_items.items() for item in items)
        formatted_total = "{:,.2f}".format(total_price)
        self.total_label.text = f"Total: €{formatted_total}"

    def clear_inputs(self):
        self.article_input.text = ""
        self.quantity_input.text = ""
        self.price_input.text = ""
        self.category_spinner.text = ""

    def clear_list(self, instance):
        self.shopping_list_manager.category_items.clear()
        self.refresh_list()

    def export_list(self, instance):
        selected_items = [item for category, items in self.shopping_list_manager.category_items.items() for item in items if item["checkbox"].active]
        if not selected_items:
            self.show_error_dialog("No hay artículos seleccionados para exportar.")
            return
        try:
            file_path = self.user_file_path_dialog()
            if file_path:
                if self.shopping_list_manager.export_list(selected_items, file_path):
                    self.show_confirmation_dialog("Lista exportada exitosamente.")
                else:
                    self.show_error_dialog("Error al exportar la lista.")
        except Exception as e:
            self.show_error_dialog(str(e))

    def user_file_path_dialog(self):
        return "shopping_list.csv"

    def show_confirmation_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def show_error_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def toggle_dark_mode(self, *args):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "BlueGray"
            self.root.ids.theme_toggle_button.text = "Light mode"
            self.root.ids.theme_toggle_button.text_color = (1, 1, 1, 1)
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"
            self.root.ids.theme_toggle_button.text = "Dark mode"
            self.root.ids.theme_toggle_button.text_color = (0, 0, 0, 1)
        self.update_welcome_label_color()
        self.update_category_label_color()


    def update_welcome_label_color(self):
        if self.theme_cls.theme_style == "Dark":
            self.root.ids.welcome_label.color = (1, 1, 1, 1)
        else:
            self.root.ids.welcome_label.color = (0, 0, 0, 1)

    def update_category_label_color(self):
        for child in self.root.ids.list_layout.children:
            if isinstance(child, Label):
                if self.theme_cls.theme_style == "Dark":
                    child.color = (1, 1, 1, 1)
                else:
                    child.color = (0, 0, 0, 1)


if __name__ == "__main__":
    ShopperApp().run()
