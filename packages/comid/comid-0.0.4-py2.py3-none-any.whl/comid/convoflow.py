from convokit import Utterance, Speaker, Corpus, TextProcessor
from tqdm import tqdm
from comid import Comid
from comid.explorer import Explorer

class ConvoCorpus(Corpus):
    comid: Comid

    def __init__(self, comid: Comid,
                 speaker_meta_keys=['author', 'author_flair_text'],
                 utt_meta_keys=['subreddit', 'depth']):

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
        super().__init__(utterances=utterances)
        self.comid = comid

class ConvoTextParser(TextProcessor):
    convoCorpus: ConvoCorpus

    def __init__(
            self,
            comid: Comid,
            model="en_core_web_sm",
            output_field="parsed",
            tags = ["NOUN", "VERB", "ADJ", "PROPN"],
            min_size=3,
            include_oc=True,
            include_comments=False,
            verbosity=1000):

        self.comid = comid
        self.tags = tags
        self.min_size = min_size
        self.include_oc = include_oc
        self.include_comments = include_comments

        self.comid.spacy_load(model)
        input_filter = lambda utt: filter_utt(utt,include_oc,include_comments)
        TextProcessor.__init__(
            self,
            proc_fn=self._process_text_wrapper,
            output_field=output_field,
            input_filter=input_filter,
            verbosity=verbosity
        )

    def _process_text_wrapper(self, text, aux_input={}):
        return process_text(
            text,
            aux_input.get("comid", self.comid),
            aux_input.get("tags", self.tags),
            aux_input.get("min_size", self.min_size),
        )

def filter_utt(utt,include_oc,include_comments):
    if utt.meta['depth'] is None:
        if include_oc:
            return True
    elif include_comments and utt.meta['depth'] == 0:
        return True
    return False

def process_text(text,comid,tags,min_size):
    return comid.text_tokenizer(text, tags=tags, min_size=min_size)