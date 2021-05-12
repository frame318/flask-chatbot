from config import *
from flask import *

assessment = Blueprint('assessment', __name__)

@assessment.route('/st5')
def st5():
    return render_template('AssessmentForm/ST5.html')

@assessment.route('/checkst5', methods=['POST'])
def checkst5():
    id = request.form['userId']
    q1= int(request.form['q1'])
    q2 = int(request.form['q2'])
    q3 = int(request.form['q3'])
    q4 = int(request.form['q4'])
    q5 = int(request.form['q5'])
    sum = q1+q2+q3+q4+q5
    if sum <= 4:
        text_message = TextSendMessage(text='ระดับความเครียด : เล็กน้อย')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : เป็นความเครียดที่เกิดขึ้นได้ในชีวิตประจำวันและสามารถปรับตัวกับสถานการณ์ต่างๆ ได้อย่างเหมาะสม')
        line_bot_api.push_message(id, [text_message,text_message2])
    elif sum > 4 and sum <=7:
        text_message = TextSendMessage(text='ระดับความเครียด : ปานกลาง')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : สามารถผ่อนคลายความเครียดด้วยการทำกิจกรรมที่เพิ่มพลังเช่น ออกกำลังกาย เล่นกีฬาทำสิ่งที่สนุกสนานเพลิดเพลิน เช่นอ่านหนังสือ ฟังเพลง ทำงานอดิเรก หรือ พูดคุยระบายความไม่สบายใจกับผู้ที่ไว้วางใจ')
        line_bot_api.push_message(id, [text_message, text_message2])
    elif sum > 7 and sum <=9:
        text_message = TextSendMessage(text='ระดับความเครียด : มาก')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : การฝึกหายใจคลายเครียด พูดคุยระบายความเครียดกับผู้ที่ไว้วางใจ หาสาเหตุหรือปัญหาที่ทำให้เกิดความเครียดและหาวิธีแก้ไข หากท่านไม่สามารถจัดการคลายเครียดด้วยตนเอง ควรปรึกษากับผู้ให้การปรึกษาในหน่วยงานต่างๆ เช่น หน่วยบริการให้การปรึกษา / คลายเครียด\n- โรงพยาบาลจิตเวชขอนแก่นราชนครินทร์\n- ความรู้สุขภาพจิต 1667, สายด่วน / Hot line 1323')
        line_bot_api.push_message(id, [text_message, text_message2])
    elif sum > 9:
        text_message = TextSendMessage(text='ระดับความเครียด : มากที่สุด')
        text_message2 = TextSendMessage(text='ควรได้รับการช่วยเหลือจากผู้ให้การปรึกษาอย่างรวดเร็ว เช่น ทางโทรศัพท์ หรือ ผู้ให้การปรึกษาในหน่วยงานต่างๆ การเข้าถึงบริการ แหล่งความช่วยเหลือมีดังนี้ หน่วยบริการให้การปรึกษา / คลายเครียด\n- โรงพยาบาลจิตเวชขอนแก่นราชนครินทร์\n- ความรู้สุขภาพจิต 1667, สายด่วน / Hot line 1323\n- ควรได้รับการช่วยเหลือจากผู้ให้การปรึกษาอย่างรวดเร็ว เช่น ทางโทรศัพท์ หรือ ผู้ให้การปรึกษาในหน่วยงานต่างๆ การเข้าถึงบริการ แหล่งความช่วยเหลือมีดังนี้')
        line_bot_api.push_message(id, [text_message, text_message2])
    return render_template('close.html')

@assessment.route('/sui9')
def sui9():
    return render_template('AssessmentForm/SUI9.html')

@assessment.route('/checksui9',methods=['POST'])
def checksui9():
    id = request.form['userId']
    q1= int(request.form['q1'])
    q2 = int(request.form['q2'])
    q3 = int(request.form['q3'])
    q4 = int(request.form['q4'])
    q5 = int(request.form['q5'])
    q6 = int(request.form['q6'])
    q7 = int(request.form['q7'])
    q8 = int(request.form['q8'])
    q9 = int(request.form['q9'])
    sum = q1+q2+q3+q4+q5+q6+q7+q8+q9
    print(id)
    if sum > 1:
        line_bot_api.push_message(id, TextSendMessage(text='มีความเสี่ยงต่อการฆ่าตัวตาย ควรขอรับบริการปรึกษาจากหน่วยงานสาธารณสุขใกล้บ้าน'))
    else:
        line_bot_api.push_message(id, TextSendMessage(text='ไม่มีความเสี่ยง'))
    return render_template('close.html')

@assessment.route('/Q8')
def Q8():
    return render_template('AssessmentForm/Q8.html')

@assessment.route('/checkQ8',methods=['POST'])
def checkQ8():
    id = request.form['userId']
    q1= int(request.form['q1'])
    q2 = int(request.form['q2'])
    q3 = int(request.form['q3'])
    try:
        q3q = int(request.form['q3q'])
    except:
        q3q = 0
    q4 = int(request.form['q4'])
    q5 = int(request.form['q5'])
    q6 = int(request.form['q6'])
    q7 = int(request.form['q7'])
    q8 = int(request.form['q8'])

    sum = q1+q2+q3+q3q+q4+q5+q6+q7+q8
    print(q3q)
    print(sum)
    if sum == 0:
        line_bot_api.push_message(id, TextSendMessage(text='ไม่มีแนวโน้มฆ่าตัวตายในปัจจุบัน'))
    elif sum >= 1 and sum <=8:
        text_message = TextSendMessage(text='เล็กน้อย')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : ควรปรึกษาหรือส่งต่อผู้ชำนาญด้านให้การปรึกษาหรือผู้ทำงานด้านสุขภาพจิตที่ได้รับการฝึกอบรมมาดีแล้วเพื่อให้การช่วยเหลือทางสังคมจิตใจ')
        line_bot_api.push_message(id, [text_message, text_message2])
    elif sum >= 9 and sum <=16:
        text_message = TextSendMessage(text='ปานกลาง')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : ควรมีญาติดูแลอย่างใกล้ชิด และให้พามาพบแพทย์ทันที')
        line_bot_api.push_message(id, [text_message, text_message2])
    elif sum >= 17 :
        text_message = TextSendMessage(text='รุนแรง')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : ควรมีญาติดูแลอย่างใกล้ชิด และให้พามาพบแพทย์ทันที')
        line_bot_api.push_message(id, [text_message, text_message2])
    return render_template('close.html')

@assessment.route('/Q9')
def Q9():
    return render_template('AssessmentForm/Q9.html')
    
@assessment.route('/checkQ9',methods=['POST'])
def checkQ9():
    id = request.form['userId']
    q1= int(request.form['q1'])
    q2 = int(request.form['q2'])
    q3 = int(request.form['q3'])
    q4 = int(request.form['q4'])
    q5 = int(request.form['q5'])
    q6 = int(request.form['q6'])
    q7 = int(request.form['q7'])
    q8 = int(request.form['q8'])
    q9 = int(request.form['q9'])

    sum = q1+q2+q3+q4+q5+q6+q7+q8+q9
    if sum < 7:
        text_message = TextSendMessage(text='ไม่มีภาวะซึมเศร้า')
        line_bot_api.push_message(id, text_message)
    elif sum >= 7 and sum <=12:
        text_message = TextSendMessage(text='ระดับน้อย')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : แนะนำวิธีการคลายเครียดด้วยตนเอง เช่น การพูดคุยระบายความรู้สึก การนวด การฟังเพลง การทำสมาธิ การผ่อนคลายกล้ามเนื้อ')
        line_bot_api.push_message(id, [text_message, text_message2])
    elif sum >= 13 and sum <=18:
        text_message = TextSendMessage(text='ระดับปานกลาง')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : แนะนำวิธีการคลายเครียดด้วยตนเอง เช่น การพูดคุยระบายความรู้สึก การนวด การฟังเพลง การทำสมาธิ การผ่อนคลายกล้ามเนื้อ\n- หากไม่ดีขึ้นให้ ให้พามาพบแพทย์ทันที')
        line_bot_api.push_message(id, [text_message, text_message2])
    elif sum >= 19:
        text_message = TextSendMessage(text='รุนแรง')
        text_message2 = TextSendMessage(text='แนวทางการดูแล : แนะนำวิธีการคลายเครียดด้วยตนเอง เช่น การพูดคุยระบายความรู้สึก การนวด การฟังเพลง การทำสมาธิ การผ่อนคลายกล้ามเนื้อ\n- หากมีความเสี่ยงต่อการฆ่าตัวตาย ควรมีญาติดูแลอย่างใกล้ชิด และให้พามาพบแพทย์ทันที')
        line_bot_api.push_message(id, [text_message, text_message2])
    return render_template('close.html')
