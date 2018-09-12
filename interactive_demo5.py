# -*- coding: utf-8 -*


#热词启动
import sound_recognize as srn
import ro_to_xf_to_ro as roxf

def main():
    while(True):
        if(
            srn.sound_recognize().sound_recognize(3)):
            pass
        else:
            continue
        results = roxf.integration_from_nao()
        roxf.str_sclassification(results)


if __name__ == '__main__':
    main()