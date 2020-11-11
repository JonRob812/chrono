UI_SOURCE_DIR = designer
RESOURCE_QRC = resource.qrc

UI_SOURCE_FILES = $(wildcard $(UI_SOURCE_DIR)/*.ui)
UI_PY_FILES = $(patsubst $(UI_SOURCE_DIR)/%.ui, ui/%_ui.py, $(UI_SOURCE_FILES))
RESOURCES = resources/resources.py

.PHONY : ui
ui: $(UI_PY_FILES)

ui/%_ui.py: $(UI_SOURCE_DIR)/%.ui
	rm -f $@
	python3 -m PyQt5.uic.pyuic -o $@ $<

.PHONY : resources
resource: $(RESOURCES)


$(RESOURCES) : $(RESOURCE_QRC)
	rm -f $@
	pyrcc5 -o $@ $<


