# Customer Segmentation with RFM

* Çalışmada amacım RFM analizi ile müşterilerin satın alma davranışlarını göz önünde bulundurarak, müşterileri segmentlere ayırmak.
  Böylece segment özelinde kararlar alınması sağlanacak,kapmanyalar düzenlenebilecektir.
  
![rfm](https://user-images.githubusercontent.com/87808313/126800670-13c12df1-0911-4d9f-93b9-eeb12e94084b.png)

# İş Problemi
* Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
pazarlama stratejileri belirlemek istemektedir.
* Örneğin şirket için çok kazançlı olan müşterileri elde tutmakiçin farklı kampanyalar, yeni müşteriler için farklı kampanyalar düzenlenmek istenmektedir.

# Veri Seti Hikayesi
* Veri seti  01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içermektedir.
* Bu projede 2010-2011 yılları arası incelenecektir.
* Bu şirketin ürün kataloğunda hediyelik eşyalar yer almaktadır.
* Şirketin müşterilerinin büyük çoğunluğu kurumsal müşterilerdir.

# Değişkenler 
* InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
* StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
* Description: Ürün ismi
* Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
* InvoiceDate: Fatura tarihi ve zamanı.
* UnitPrice: Ürün fiyatı (Sterlin cinsinden)
* CustomerID: Eşsiz müşteri numarası
* Country: Ülke ismi. Müşterinin yaşadığı ülke.

Kaggle:
https://www.kaggle.com/haticeebraralc/crm-analytics
