import var
import conexion
from PyQt5 import QtWidgets, QtCore
from time import sleep

class Ventas:

    def altaFactura(self):
        try:
            dni = var.ui.editDniclifac.text()
            fecha = var.ui.editDatafac.text()
            apel = var.ui.editApelclifac.text()
            if dni != '' and fecha != '':
                conexion.Conexion.altaFac(dni, fecha, apel)
            conexion.Conexion.mostrarFacturas(self)
        except Exception as error:
            print('Error alta factura %s' % str(error))
            return None

    def abrirCalendar(self):
        '''
        Abrir la ventana calendario
        '''
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    def cargarFechafac(qDate):
        ''''
        Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked de calendar
        '''
        try:
            if var.ui.tabWidget.currentIndex() == 1:
                data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
                var.ui.editDatafac.setText(str(data))
                var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha factura: %s ' % str(error))

    def cargarFact(self):
        '''
        Módulo que carga los datos de la factura y cliente
        :return:
        '''
        try:
            var.subfac = 0.00
            var.fac = 0.00
            var.iva = 0.00
            fila = var.ui.tabFac.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codf = fila[0]
            var.ui.lblNumFac.setText(str(codf))
            var.ui.editDatafac.setText(str(fila[1]))
            conexion.Conexion.cargarFac(str(codf))
        except Exception as error:
            print('Error cargar Facctura: %s ' % str(error))

    def prepararTablaventas(index):
        '''
        Modulo que prepara tabla Ventas, carga un combo en la tabla
        y carga dicho combo con los datos del producto
        :return:
        '''
        try:
            var.cmbventa = QtWidgets.QComboBox()
            var.ui.tabVenta.setRowCount(index + 1)
            var.ui.tabVenta.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tabVenta.setCellWidget(index, 1, var.cmbventa)
            var.ui.tabVenta.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tabVenta.setItem(index, 3, QtWidgets.QTableWidgetItem())

        except Exception as error:
            print('Error Preparar tabla de ventas: %s ' % str(error))


    def procesoVenta(self):
        try:
            row = var.ui.tabVenta.currentRow()
            codfac = var.ui.lblNumFac.text()
            articulo = var.cmbventa.currentText()
            cantidad = var.ui.tabVenta.item(row, 2).text()
            cantidad = cantidad.replace(',', '.')
            dato = conexion.Conexion.obtenCodPrec(articulo)
            subtotal = round(float(cantidad)*float(dato[1]), 2)
            var.ui.tabVenta.setItem(row, 3,QtWidgets.QTableWidgetItem(str(subtotal)))
            venta = [codfac, dato[0], cantidad]
            var.ui.tabVenta.setItem(row, 1, QtWidgets.QTableWidgetItem(str(articulo)))
            row = row + 1
            var.ui.tabVenta.insertRow(row)
            var.ui.tabVenta.setCellWidget(row, 1, var.cmbventa)
            var.ui.tabVenta.scrollToBottom()
            conexion.Conexion.cargarCmbventa()
            #sleep(1)
            if codfac != '' and articulo != '' and cantidad != '':
                conexion.Conexion.altaVenta(venta)
                var.subfac = round(float(subtotal) + float(var.subfac),2)
                var.ui.lblSubtotal.setText(str(var.subfac))
                var.iva = round(float(var.subfac) * 0.21, 2)
                var.ui.lblIva.setText(str(var.iva))
                var.fac = round(float(var.iva) + float(var.subfac), 2)
                var.ui.lblTotal.setText(str(var.fac))
            else:
               var.ui.lblstatus.setText('Faltan Datos de la Factura')

        except Exception as error:
            print('Error proceso venta: %s ' % str(error))

    def mostrarVentasfac():
        try:
            codfac = var.ui.lblNumFac.text()
            conexion.Conexion.listadoVentasfac(codfac)
            conexion.Conexion.cargarCmbventa()
        except Exception as error:
            print('Error proceso mostrar ventas por factura: %s' %str(error))
