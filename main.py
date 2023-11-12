import logging
import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

# ロガーの設定
logger = logging.getLogger('TfPoseEstimator-Video')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# パラメータの直接指定
video_file = '125449.mp4'  # 動画ファイルのパス
resize = '0x0'  # リサイズの指定（例: '432x368'）
resize_out_ratio = 4.0  # 出力サイズのリサイズ比
model = 'cmu'  # 使用するモデル
show_process = False  # プロセスの表示

# モデルのロード
w, h = model_wh(resize)
if w == 0 or h == 0:
    e = TfPoseEstimator(get_graph_path(model), target_size=(432, 368))
else:
    e = TfPoseEstimator(get_graph_path(model), target_size=(w, h))

# 動画ファイルを読み込む
cap = cv2.VideoCapture(video_file)

# 動画書き出し用の設定
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 30, (w, h))

# 動画の処理
while cap.isOpened():
    ret_val, image = cap.read()

    if not ret_val:
        break

    # 姿勢推定の実行
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)

    # 姿勢の描画
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

    # 結果の保存
    # out.write(image)

    # 結果の表示
    cv2.imshow('tf-pose-estimation result', image)

    # qを押して終了
    if cv2.waitKey(1) == ord('q'):
        break

# 終了処理
cap.release()
# out.release()
cv2.destroyAllWindows()
