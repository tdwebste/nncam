import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.PixelWriter;
import javafx.scene.image.PixelFormat;
import javafx.scene.control.Alert;
import javafx.scene.control.CheckBox;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import java.nio.ByteBuffer;

public class javafx extends Application {
    private static nncam _cam;
    private static String _name;
    private static byte[] _buf;
    private static Canvas _canvas;
    private static int _total;
    private static Stage _stage;
    private static int[] _size;

    @Override
    public void start(Stage stage) {
        _stage = stage;
        _stage.setOnCloseRequest(event -> {
            if (_cam != null) {
                _cam.close();
                _cam = null;
            }
        });

        BorderPane b = new BorderPane();
        Scene scene = new Scene(b);
        _stage.setWidth(800);
        _stage.setHeight(600);
        b.prefHeightProperty().bind(scene.heightProperty());
        b.prefWidthProperty().bind(scene.widthProperty());
        createAndShow(b);
        _stage.setScene(scene);
        _stage.show();
    }

    private static void OnEventImage() {
        if (_cam != null) {
            boolean bok = false;
            try {
                _cam.PullImageWithRowPitchV2(_buf, 24, _size[0] * 3, null);
                ++_total;
                bok = true;
            } catch (nncam.HRESULTException ex) {
                Alert alert = new Alert(Alert.AlertType.WARNING, ex.toString());
                alert.showAndWait();
            }
            if (bok) {
                /* https://docs.oracle.com/javase/8/javafx/graphics-tutorial/image_ops.htm */
                GraphicsContext gc = _canvas.getGraphicsContext2D();
                PixelWriter pw = gc.getPixelWriter();
                PixelFormat<ByteBuffer> pixelFormat = PixelFormat.getByteRgbInstance();
                pw.setPixels(0, 0, _size[0], _size[0], pixelFormat, _buf, 0, _size[0] * 3);
                _stage.setTitle(_name + ": " + _total);
            }
        }
    }

    private static void createAndShow(BorderPane b) {
        CheckBox checkAutoExposure = new CheckBox("Auto Exposure");
        checkAutoExposure.selectedProperty().addListener(new ChangeListener<Boolean>() {
            public void changed(ObservableValue<? extends Boolean> ov, Boolean old_val, Boolean new_val) {
                if (_cam != null) {
                    try {
                        _cam.put_AutoExpoEnable(checkAutoExposure.isSelected());
                    } catch (nncam.HRESULTException ex) {
                        Alert alert = new Alert(Alert.AlertType.WARNING, ex.toString());
                        alert.showAndWait();
                    }
                }
            }
        });
        b.setTop(checkAutoExposure);

        _canvas = new Canvas(800, 560);
        b.setCenter(_canvas);

        nncam.InstanceV2[] arr = nncam.EnumV2();
        if (arr.length <= 0)
            _stage.setTitle("no camera found");
        else {
            _name = arr[0].displayname;
            _stage.setTitle(_name + ": 0");
            _cam = nncam.Open(arr[0].id);
            if (_cam != null) {
                try {
                    checkAutoExposure.setSelected(_cam.get_AutoExpoEnable());
                    _size = _cam.get_Size();
                    _buf = new byte[_size[0] * _size[1] * 3];
                    _cam.StartPullModeWithCallback(new nncam.IEventCallback() {
                        /* the vast majority of callbacks come from nncam.dll/so/dylib internal threads */
                        @Override
                        public void onEvent(int nEvent, Object obj) {
                            if (nncam.EVENT_IMAGE == nEvent) {
                                Platform.runLater(new Runnable() {
                                    @Override
                                    public void run() {
                                        /* run in the UI thread */
                                        OnEventImage();
                                    }
                                });
                            }
                        }
                    }, null);
                } catch (nncam.HRESULTException ex) {
                    Alert alert = new Alert(Alert.AlertType.WARNING, ex.toString());
                    alert.showAndWait();
                }
            }
        }

        checkAutoExposure.setDisable(_cam == null);
    }

    public static void main(String[] args) {
        launch();
    }
}