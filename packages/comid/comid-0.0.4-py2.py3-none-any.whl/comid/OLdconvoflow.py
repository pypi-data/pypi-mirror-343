from convokit import Utterance, Speaker, Corpus, TextProcessor
from tqdm import tqdm

from comid import Comid
from comid.explorer import Explorer


def filter_utt(utt, include_oc, include_comments):
    if utt.meta['depth'] is None:
        if include_oc:
            return True
    elif include_comments and utt.meta['depth'] == 0:
        return True
    return False

def proc_text_utt(text,aux_input):
    print("processing text")
    return aux_input['comid'].text_tokenizer(text,tags = aux_input['tags'],min_size= aux_input['min_size'])

class ConvoFlow:
    convo_corpus: Corpus
    comid: Comid

    def __init__(self, comid: Comid,
                 speaker_meta_keys= ['author','author_flair_text'],
                 utt_meta_keys= ['subreddit','depth']):

        utterances = []
        speakers = {}
        explorer = Explorer(comid.posts)

        if 'subreddit' not in utt_meta_keys:
            utt_meta_keys.append('subreddit')
        if 'depth' not in utt_meta_keys:
            utt_meta_keys.append('depth')

        for oc, replies in tqdm(explorer.thread_replies.items(), "Creating convokit data"):
            if comid.posts[oc]['author_id'] not in speakers:
                speakers[comid.posts[oc]['author_id']] = Speaker(id=comid.posts[oc]['author_id'], meta={
                    key: comid.posts[oc][key] if key in comid.posts[oc] else None for key in speaker_meta_keys
                })
            utterances.append(Utterance(
                id=oc,
                speaker=speakers[comid.posts[oc]['author_id']],
                conversation_id=oc,
                timestamp=comid.posts[oc]['created'],
                text=comid.posts[oc]['full_text'],
                meta={
                    key: comid.posts[oc][key] if key in comid.posts[oc] else None for key in utt_meta_keys
                }
            ))
            for reply in replies:
                if comid.posts[reply]['author_id'] not in speakers:
                    speakers[comid.posts[reply]['author_id']] = Speaker(id=comid.posts[reply]['author_id'], meta={
                        key: comid.posts[reply][key] if key in comid.posts[reply] else None for key in speaker_meta_keys
                    })
                utterances.append(Utterance(
                    id=reply,
                    speaker=speakers[comid.posts[reply]['author_id']],
                    conversation_id=oc,
                    reply_to=comid.posts[reply]['parent_id'],
                    timestamp=comid.posts[reply]['created'],
                    text=comid.posts[reply]['full_text'],
                    meta={
                        key: comid.posts[reply][key] if key in comid.posts[reply] else None for key in utt_meta_keys
                    }
                ))
        self.convo_corpus = Corpus(utterances=utterances)
        self.comid = comid

    def get_convo_corpus(self):
        return self.convo_corpus

    def text_parser(self,tags = ["NOUN", "VERB", "ADJ", "PROPN"], min_size=3,include_oc=True,include_comments=False):

        text_processor = TextProcessor(proc_fn=proc_text_utt, input_field="text", output_field='words', verbosity=1000,
                                       aux_input={"comid": self.comid,"tags": tags,"min_size":min_size},
                                       input_filter=lambda utt: filter_utt(utt,include_oc=include_oc,include_comments=include_comments))
        self.convo_corpus = text_processor.transform(self.convo_corpus)






