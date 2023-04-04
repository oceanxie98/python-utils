from keras import backend as K


class Config:

    # def __init__(self):
    #     self.anchor_box_scales = [128, 256, 512] #[128, 256, 512] [16,32,64]    #先验框参数
    #     self.anchor_box_ratios = [[1, 1], [1, 2], [2, 1]]   #先验框参数
    #     self.rpn_stride = 16    #先验框参数16
    #     self.num_rois = 32  #每一次输入进来的建议框数量32
    #     self.verbose = True
    #     self.model_path = "logs/model.h5"
    #     self.rpn_min_overlap = 0.3 #0.3 0.05  #utils的参数，最小重合先验框与真实框的重合程度0.3
    #     self.rpn_max_overlap = 0.7 #0.7 0.1 #utils的参数，最大重合0.7
    #     self.classifier_min_overlap = 0.1
    #     self.classifier_max_overlap = 0.5 # 建议框和真实框重合程度
    #     self.classifier_regr_std = [8.0, 8.0, 4.0, 4.0]

    def __init__(self):
        self.anchor_box_scales = [8,16,32] #[128, 256, 512] [16,32,64]    #先验框参数
        self.anchor_box_ratios = [[1, 1], [1, 1.5], [1.5, 1]]   #先验框参数
        self.rpn_stride = 16    #先验框参数16
        self.num_rois = 32  #每一次输入进来的建议框数量32
        self.verbose = True
        self.model_path = "logs/model.h5"
        self.rpn_min_overlap = 0.01 #0.3 0.05  #utils的参数，最小重合先验框与真实框的重合程度0.3
        self.rpn_max_overlap = 0.1 #0.7 0.1 #utils的参数，最大重合0.7
        self.classifier_min_overlap = 0.1
        self.classifier_max_overlap = 0.5 # 建议框和真实框重合程度
        self.classifier_regr_std = [8.0, 8.0, 4.0, 4.0]

        