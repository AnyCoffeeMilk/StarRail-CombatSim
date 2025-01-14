def saveAs(self):
    if not self.isWindowModified():
        return
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
        self, "Save File", "", "All Files(*);;Text Files(*.txt)", options=options
    )
    if fileName:
        with open(fileName, "w") as f:
            f.write(self.editor.toPlainText())
        self.fileName = fileName
        self.setWindowTitle(str(os.path.basename(fileName)) + " - Notepad Alpha[*]")
