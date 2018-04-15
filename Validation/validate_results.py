from Validation.validate_data import ValidateData

class ValidateResults(object):

    eval_lens = None
    eval_cornea = None
    has_lens = None

    def __init__(self, name):
        top, bot, has_lens = ValidateData._load_validation(name)
        self.eval_lens = top
        self.eval_cornea = bot
        self.has_lens = has_lens

    def validate(self, result):

        tp = fn = fp = tn = mse = mae = n = 0

        if self.has_lens and result.n_capas < 3:
            tp +=1
        elif self.no_lens and result.n_capas == 3:
            fn +=1
        elif not self.no_lens and result.n_capas < 3:
            fp += 1
        elif not self.no_lens:
            tn += 1
            mse_img, mae_img, n_img = self._get_error(result.lens,result.cornea,self.eval_lens,self.eval_cornea)
            mse += mse_img
            mae += mae_img
            n += n_img

        mse = mse/n
        acc, tpr, tnr, ppv, npv = self._get_metrics(tp,tn,fp,fn)

        return {mse: mse, acc: acc, tpr: tpr, tnr: tnr, ppv: ppv, npv: npv}

    def _get_metrics(self, tp, tn, fp, fn):
        tpr = tp / (tp + fn) # sensitivity or true positive rate
        tnr = tn / (tn + fp) # specifity or true negative rate
        ppv = tp / (tp + fp) # precision or positive predictive value
        npv = tn / (tn + fn) # negative preditive value
        acc = (tp + tn) / (tp + tn + fp + fn) # accuracy
        return acc, tpr, tnr, ppv, npv

    def _get_error(self, result, top_line, bot_line):
        # Return Mean Square Error and Mean Absolute Error
        mse = mae = 0
        n = len(top_line) + len(bot_line)

        for x,y in top_line:
            pred = result.get_lens_pos(x)
            if pred > -1:
                res = y - pred
                mse += (res)**2
                mae += abs(res)

        for x,y in bot_line:
            pred = result.get_cornea_pos(x)
            if pred > 1:
                res = y - pred
                mse += (res)**2
                mae += abs(res)

        return mse, mae, n